"""El repo no debe filtrar datos personales al commitear.

Esto no sustituye a pensar. Es la red de seguridad para cuando el cansancio gana:
falla en el commit, no en un repo publico tres meses despues.

Que detecta:
  - Emails
  - Telefonos españoles
  - DNI y NIE
  - URLs de linkedin.com/in/
  - Rutas C:\\Users\\ y /home/
  - Palabras de tu lista personal (config.toml o config.example.toml)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# --- Patrones ----------------------------------------------------------------

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Telefono movil o fijo español, con o sin prefijo.
TELEFONO_ES = re.compile(
    r"(?<![\d\w])"
    r"(?:\+34[\s-]?)?"
    r"[6-9]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}"
    r"(?![\d\w])"
)

# 8 digitos con letra, con o sin guion. Cubre DNI y NIE.
DNI_NIE = re.compile(
    r"(?<![\w-])"
    r"\d{8}"
    r"[-]?"
    r"[A-HJ-NP-TV-Z]"
    r"(?![\w-])",
    re.IGNORECASE,
)

LINKEDIN_IN = re.compile(r"linkedin\.com/in/[\w.-]+", re.IGNORECASE)
RUTA_WINDOWS = re.compile(r"[A-Za-z]:\\Users\\[\w.-]+", re.IGNORECASE)
RUTA_UNIX = re.compile(r"/home/[\w.-]+/|/Users/[\w.-]+/")

# --- Falsos positivos conocidos ------------------------------------------------

# Dominios reservados por la RFC 2606 para documentacion. example.com no
# pertenece a nadie: un email ahi nunca es un dato real.
DOMINIOS_RESERVADOS = (
    "example.com", "example.org", "example.net", "example.edu",
    "localhost", "invalid", "test",
)

# Placeholders que aparecen literalmente en las plantillas.
EMAIL_PERMITIDO = {
    "ejemplo@example.com",
    "user@example.com",
    "tu@email.com",
    "correo@example.com",
}


def email_es_de_ejemplo(direccion: str) -> bool:
    """True si la direccion usa un dominio reservado o contiene 'ejemplo'."""
    if direccion.lower() in EMAIL_PERMITIDO:
        return True
    _, _, dominio = direccion.rpartition("@")
    dominio = dominio.lower()
    return (any(dominio == d or dominio.endswith("." + d) for d in DOMINIOS_RESERVADOS)
            or "ejemplo" in dominio)

# Ficheros donde los patrones son parte del ejemplo, no datos reales.
EXCLUIDOS = {
    ".git/",
    ".pytest_cache/",
    "__pycache__/",
    "node_modules/",
    ".venv/",
    "venv/",
    "4-ofertas/pipeline.csv",
    "4-ofertas/pipeline.csv.bak",
    "4-ofertas/config.toml",
    "datos-personales/",
    "mis-datos/",
    "_archivo/",
}

EXTENSIONES = {
    ".md", ".py", ".txt", ".csv", ".json", ".yml", ".yaml",
    ".toml", ".cfg", ".ini", ".html", ".sh", ".js", ".ts",
}


# Ficheros que documentan el propio escaner. Contienen los patrones como
# ejemplo, asi que aparecer ahi es exactamente lo que queremos.
DOCUMENTAN_EL_ESCANER = {
    "scripts/check-privacidad.py",
    "PRIVACY.md",
    "SECURITY.md",
}

# En estos ficheros los marcadores de plantilla son instrucciones, no datos.
MARCADOR = re.compile(r"\[TU_[\w]+\]|\[TU\]|\{\{.*?\}\}|<[A-Z_]+>")


def es_ilustracion(ruta_rel: str, linea: str) -> bool:
    """True si el patron aparece como ejemplo, no como dato real."""
    if ruta_rel in DOCUMENTAN_EL_ESCANER:
        return True
    # Rutas recortadas: "C:\Users\..." es documentacion, no una ruta real.
    if "..." in linea or "…" in linea:
        return True
    return bool(MARCADOR.search(linea))


class Hallazgo:
    def __init__(self, fichero: Path, linea: int, regla: str, texto: str):
        self.fichero = fichero
        self.linea = linea
        self.regla = regla
        self.texto = texto

    def __str__(self) -> str:
        rel = self.fichero.relative_to(REPO_ROOT)
        return f"{rel}:{self.linea}  [{self.regla}]  {self.texto.strip()[:70]}"


def cargar_palabras_prohibidas() -> list[str]:
    """De donde leer tus palabras privadas.

    Prioridad: config.toml (privada, tiene tus datos), luego config.example.toml.
    """
    palabras: list[str] = []

    for nombre in ("config.toml", "config.example.toml"):
        ruta = REPO_ROOT / "4-ofertas" / nombre
        if not ruta.exists():
            continue
        dentro = False
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            sin_comentario = linea.split("#", 1)[0].strip()

            if not dentro:
                if sin_comentario.startswith("palabras_prohibidas"):
                    dentro = True
                    resto = sin_comentario.split("=", 1)[1] if "=" in sin_comentario else "["
                    if "]" in resto:
                        break
                continue

            # Una linea "[" abre la lista sin cerrarla todavia.
            if sin_comentario.startswith("]"):
                break
            # Otra seccion del TOML: la lista se quedo vacia o sin cerrar.
            if sin_comentario.startswith("["):
                break

            limpio = sin_comentario.strip().strip(",").strip("[]\"'")
            if limpio:
                palabras.append(limpio)

    return [p for p in palabras if len(p) >= 3]


def ficheros_a_revisar(raiz: Path) -> list[Path]:
    encontrados: list[Path] = []
    for ruta in raiz.rglob("*"):
        if not ruta.is_file():
            continue
        rel = ruta.relative_to(raiz).as_posix()
        if any(rel.startswith(excl) for excl in EXCLUIDOS):
            continue
        if ruta.suffix.lower() not in EXTENSIONES:
            continue
        encontrados.append(ruta)
    return encontrados


def revisar_fichero(ruta: Path, palabras: list[str]) -> list[Hallazgo]:
    hallazgos: list[Hallazgo] = []
    try:
        lineas = ruta.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return hallazgos

    rel = ruta.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in ruta.parents else ruta.name

    for numero, linea in enumerate(lineas, start=1):
        if es_ilustracion(rel, linea):
            continue

        for coincidencia in EMAIL.finditer(linea):
            if not email_es_de_ejemplo(coincidencia.group()):
                hallazgos.append(Hallazgo(ruta, numero, "email", coincidencia.group()))

        for coincidencia in TELEFONO_ES.finditer(linea):
            digitos = re.sub(r"\D", "", coincidencia.group())
            # Descarta numeros de ejemplo usados en la documentacion de scripts.
            if digitos.endswith("0000000"):
                continue
            hallazgos.append(Hallazgo(ruta, numero, "telefono-es", coincidencia.group()))

        for coincidencia in DNI_NIE.finditer(linea):
            hallazgos.append(Hallazgo(ruta, numero, "dni-nie", coincidencia.group()))

        for coincidencia in LINKEDIN_IN.finditer(linea):
            hallazgos.append(Hallazgo(ruta, numero, "linkedin", coincidencia.group()))

        for coincidencia in RUTA_WINDOWS.finditer(linea):
            hallazgos.append(Hallazgo(ruta, numero, "ruta-windows", coincidencia.group()))

        for coincidencia in RUTA_UNIX.finditer(linea):
            hallazgos.append(Hallazgo(ruta, numero, "ruta-unix", coincidencia.group()))

        for palabra in palabras:
            if palabra.lower() in linea.lower():
                hallazgos.append(Hallazgo(ruta, numero, "palabra-prohibida", palabra))

    return hallazgos


def main() -> int:
    ap = argparse.ArgumentParser(description="Comprueba que no hay datos personales")
    ap.add_argument("--path", type=Path, default=None, help="Ruta a revisar")
    ap.add_argument("--todo", action="store_true",
                    help="Revisa todo el repo, no solo lo que se va a commitear")
    args = ap.parse_args()

    raiz = REPO_ROOT

    if args.todo or args.path:
        ficheros = ficheros_a_revisar(raiz if not args.path else args.path)
        modo = "todo el repositorio"
    else:
        # Solo lo staged o modificado: lo que va a acabar en el commit.
        resultado = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=raiz, capture_output=True, text=True,
        )
        if resultado.returncode != 0:
            ficheros = ficheros_a_revisar(raiz)
            modo = "todo el repositorio (no se pudo consultar git)"
        else:
            nombres = [n for n in resultado.stdout.split() if n]
            ficheros = [raiz / n for n in nombres if (raiz / n).exists()]
            ficheros = [f for f in ficheros if f.suffix.lower() in EXTENSIONES]
            modo = "ficheros preparados para commit"

    palabras = cargar_palabras_prohibidas()

    print(f"Revisando {len(ficheros)} ficheros ({modo})")
    print(f"Palabras personales activas: {len(palabras)}")
    print()

    todos: list[Hallazgo] = []
    for fichero in ficheros:
        todos.extend(revisar_fichero(fichero, palabras))

    if not todos:
        print("OK: no se ha encontrado ningun dato personal.")
        return 0

    print(f"{len(todos)} hallazgo(s):")
    print()
    for hallazgo in sorted(todos, key=lambda h: str(h.fichero)):
        print(f"  {hallazgo}")

    print()
    print("Como resolverlo:")
    print("  - Usa marcadores: [TU_NOMBRE], [TU_EMAIL], [TU_USUESTO]")
    print("  - Revisa PRIVACY.md")
    print("  - Si es un dato que debe estar, anadelo a EXCLUIDOS en este script")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
