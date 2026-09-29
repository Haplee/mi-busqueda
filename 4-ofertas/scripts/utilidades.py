"""Utilidades compartidas por los scripts de mi-busqueda.

Reglas de este modulo:
  - Ninguna ruta absoluta. Todo se resuelve relativo a la raiz del repo.
  - Ninguna preferencia personal en el codigo. Todo sale de config.toml.
  - Ningun estado protegido se puede modificar por error.
"""

from __future__ import annotations

import csv
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

# --- Rutas ------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).resolve().parent
OFERTAS_DIR = SCRIPTS_DIR.parent
REPO_ROOT = OFERTAS_DIR.parent


# --- Estados ----------------------------------------------------------------

ESTADOS = (
    "Detectada",
    "Revisada",
    "Interesante",
    "Ajustada",
    "Enviada",
    "SinRespuesta",
    "Seguimiento",
    "Entrevista",
    "PruebaTecnica",
    "Oferta",
    "Rechazada",
    "Descartada",
)

#: Estados que jamas deben ser modificados por un script automatico.
#: Una candidatura que ya has enviado es historico: si un script la reescribe,
#: se pierde el registro de lo que paso de verdad.
#:
#: Sin acentos, porque el pipeline es un CSV que se abre en Excel y en un
#: editor de texto, y las dos cosas noacetan lo mismo.
ESTADOS_PROTEGIDOS = frozenset(
    {"Enviada", "Seguimiento", "Entrevista", "PruebaTecnica", "Oferta"}
)

#: Variantes con acentos o mayusculas, aceptadas al leer un pipeline ya
#: existente. Se normalizan al escribir, para no propagar variantes.
ALIAS_ESTADOS = {
    "Prueba Técnica": "PruebaTecnica",
    "PruebaTecnica": "PruebaTecnica",
    "pruebatecnica": "PruebaTecnica",
    "prueba técnica": "PruebaTecnica",
    "Prueba": "PruebaTecnica",
    "prueba": "PruebaTecnica",
    "Prueba tecnica": "PruebaTecnica",
}

#: Estado que marca una fila como demo. No cuenta en las metricas.
ESTADO_EJEMPLO = "EJEMPLO"


# --- Esquema del pipeline ----------------------------------------------------

COLUMNAS = (
    "ID",
    "Fecha",
    "Empresa",
    "Puesto",
    "Ubicacion",
    "Modalidad",
    "Contrato",
    "Salario",
    "Fuente",
    "URL",
    "Estado",
    "Contacto",
    "ProximaAccion",
    "FechaSeguimiento",
    "Encaje",
    "Notas",
)


class PipelineError(Exception):
    """Error legible de pipeline o de configuracion."""


class EstadoProtegidoError(PipelineError):
    """Una escritura iba a tocar una candidatura ya enviada.

    Hereda de PipelineError a proposito: los scripts ya la capturan y la
    muestran como error legible, sin tratar este caso como una excepcion.
    """


# --- Normalizacion de texto --------------------------------------------------

_NO_ASCII = re.compile(r"[^\w\s-]", re.UNICODE)
_ESPACIOS = re.compile(r"[\s_]+")


def normalizar(texto: str) -> str:
    """Quita acentos, pasa a minusculas y colapsa espacios.

    Se usa para comparar ubicaciones y modalidades sin depender de como las
    escribio cada portal: "Madrid", "madrid" y "MADRID" tienen que coincidir.
    """
    if texto is None:
        return ""
    descompuesto = unicodedata.normalize("NFKD", str(texto))
    sin_acentos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    limpio = _NO_ASCII.sub(" ", sin_acentos).lower()
    return _ESPACIOS.sub(" ", limpio).strip()


# --- Lectura del config ------------------------------------------------------


@dataclass(frozen=True)
class Config:
    """Preferencias del usuario, leidas de config.toml.

    Se lee con tomllib (stdlib desde Python 3.11). No hay dependencias externas.
    """

    busqueda_keywords: tuple[str, ...]
    busqueda_exclude: tuple[str, ...]
    modalidades: tuple[str, ...]
    contratos: tuple[str, ...]
    salario_minimo: int
    estados_ejemplo: frozenset[str]
    palabras_prohibidas: tuple[str, ...]
    umbral_interesante: int
    fuentes_activas: tuple[str, ...]
    path: Path | None = None

    @classmethod
    def cargar(cls, path: Path | str | None = None) -> "Config":
        """Lee config.toml. Si no existe, devuelve valores vacios neutros.

        Devolver una config neutra en vez de fallar permite que los scripts
        se puedan ejecutar para inspeccionar un CSV recien creado.
        """
        ruta = Path(path) if path else Path(OFERTAS_DIR) / "config.toml"
        if not ruta.exists():
            return cls._vacio(ruta)

        try:
            import tomllib
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise PipelineError(
                "Necesitas Python 3.11 o superior para leer config.toml."
            ) from exc

        with ruta.open("rb") as fh:
            datos = tomllib.load(fh)

        busqueda = datos.get("busqueda", {})
        prefs = datos.get("preferencias", {})
        scoring = datos.get("scoring", {})
        fuentes = datos.get("fuentes", {})
        privacidad = datos.get("privacidad", {})

        ejemplo = privacidad.get("estado_ejemplo", ESTADO_EJEMPLO)

        return cls(
            busqueda_keywords=tuple(busqueda.get("keywords", ())),
            busqueda_exclude=tuple(busqueda.get("exclude_keywords", ())),
            modalidades=tuple(prefs.get("modalidades", ())),
            contratos=tuple(prefs.get("contratos", ())),
            salario_minimo=int(prefs.get("salario_minimo", 0) or 0),
            estados_ejemplo=frozenset({str(ejemplo)}),
            palabras_prohibidas=tuple(privacidad.get("palabras_prohibidas", ())),
            umbral_interesante=int(scoring.get("umbral_interesante", 7)),
            fuentes_activas=tuple(fuentes.get("activas", ())),
            path=ruta,
        )

    @classmethod
    def _vacio(cls, ruta: Path) -> "Config":
        return cls(
            busqueda_keywords=(),
            busqueda_exclude=(),
            modalidades=(),
            contratos=(),
            salario_minimo=0,
            estados_ejemplo=frozenset({ESTADO_EJEMPLO}),
            palabras_prohibidas=(),
            umbral_interesante=7,
            fuentes_activas=(),
            path=None,
        )


# --- Lectura y escritura del pipeline ----------------------------------------


def ruta_pipeline(repo_root: Path | None = None) -> Path:
    base = Path(repo_root) if repo_root else OFERTAS_DIR
    return base / "pipeline.csv"


def ruta_ejemplo(repo_root: Path | None = None) -> Path:
    base = Path(repo_root) if repo_root else OFERTAS_DIR
    return base / "pipeline.example.csv"


def ruta_backup(ruta_csv: Path) -> Path:
    """Backup rotativo: un unico fichero, pipeline.csv.bak.

    El patron pipeline.csv.bak-AAAAMMDD-HHMMSS genera cientos de ficheros y no
    ayuda a nada: solo tienes un backup util, el anterior a la ultima
    modificacion.
    """
    return ruta_csv.with_suffix(ruta_csv.suffix + ".bak")


def crear_backup(ruta_csv: Path) -> Path | None:
    """Copia el CSV a pipeline.csv.bak. Devuelve None si no habia CSV."""
    if not ruta_csv.exists():
        return None
    destino = ruta_backup(ruta_csv)
    shutil.copy2(ruta_csv, destino)
    return destino


def leer_pipeline(ruta_csv: Path) -> list[dict[str, str]]:
    """Lee el pipeline como lista de dicts. No modifica nada."""
    if not ruta_csv.exists():
        raise PipelineError(
            f"No existe {ruta_csv.name}. Copia pipeline.example.csv a pipeline.csv."
        )

    with ruta_csv.open(newline="", encoding="utf-8-sig") as fh:
        lector = csv.DictReader(fh)
        faltan = [c for c in COLUMNAS if c not in (lector.fieldnames or [])]
        if faltan:
            raise PipelineError(
                "El pipeline no tiene todas las columnas esperadas. Faltan: "
                + ", ".join(faltan)
            )
        filas = [dict(fila) for fila in lector]
    for fila in filas:
        normalizada = ALIAS_ESTADOS.get(fila.get("Estado", "").strip())
        if normalizada:
            fila["Estado"] = normalizada
    return filas


def _estado_protegido(fila: dict[str, str]) -> bool:
    return ALIAS_ESTADOS.get(fila.get("Estado", "").strip(),
                              fila.get("Estado", "").strip()) in ESTADOS_PROTEGIDOS


def comprobar_protegidas(
    antes: list[dict[str, str]], despues: list[dict[str, str]]
) -> None:
    """Falla si una escritura cambia una fila en estado protegido.

    Que exista el backup no es suficiente: el backup está para cuando algo sale
    mal, y lo que tiene que salir mal aquí es la escritura, no la recuperación
    posterior. Si un script cambia una candidatura que ya has enviado, el
    registro histórico deja de servir para nada.
    """
    indice_antes = {f.get("ID", ""): f for f in antes}
    indice_despues = {f.get("ID", ""): f for f in despues}

    cambios: list[str] = []
    for id_fila, previa in indice_antes.items():
        if id_fila not in indice_despues:
            cambios.append(f"{id_fila}: eliminada")
            continue
        actual = indice_despues[id_fila]
        if not _estado_protegido(previa):
            continue
        for columna in COLUMNAS:
            if previa.get(columna, "") != actual.get(columna, ""):
                cambios.append(
                    f"{id_fila}: {columna} "
                    f"{previa.get(columna, '')!r} -> {actual.get(columna, '')!r}"
                )

    if cambios:
        detalle = "\n  - ".join(cambios)
        raise EstadoProtegidoError(
            "La escritura cambiaria filas en estado protegido "
            f"({', '.join(sorted(ESTADOS_PROTEGIDOS))}):\n  - {detalle}\n"
            "Una candidatura enviada es un registro historico. "
            "Si el cambio es legitimo, hazlo a mano en el CSV."
        )


def escribir_pipeline(ruta_csv: Path, filas: list[dict[str, str]]) -> Path | None:
    """Escribe el pipeline creando antes un backup rotativo.

    Este es el UNICO punto del repo que escribe en pipeline.csv a proposito:
    todas las escrituras pasan por aqui y, por tanto, por el backup y por la
    comprobacion de estados protegidos.
    """
    if ruta_csv.exists():
        comprobar_protegidas(leer_pipeline(ruta_csv), filas)

    backup = crear_backup(ruta_csv)

    with ruta_csv.open("w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=list(COLUMNAS))
        escritor.writeheader()
        for fila in filas:
            fila = dict(fila)
            fila["Estado"] = ALIAS_ESTADOS.get(
                fila.get("Estado", "").strip(), fila.get("Estado", "").strip()
            )
            escritor.writerow({c: fila.get(c, "") for c in COLUMNAS})

    return backup


# --- Claves y fechas ---------------------------------------------------------


def generar_id(empresa: str, puesto: str, fecha: date | None = None) -> str:
    """ID unico y legible: AAAA-MM-DD_EMPRESA_PUESTO.

    Los puntos se convierten en guiones, no en separadores: "Empresa S.L."
    produce "empresa-s-l", que evita que el ID se lea como tres campos.
    """
    dia = fecha or date.today()

    def slug(texto: str) -> str:
        base = normalizar(texto).replace(" ", "-").replace(".", "-")
        limpio = re.sub(r"-{2,}", "-", base).strip("-")
        return limpio[:40] or "sin-nombre"

    return f"{dia.isoformat()}_{slug(empresa)}_{slug(puesto)}"


def parsear_fecha(valor: str) -> date | None:
    """Parsea AAAA-MM-DD. Devuelve None si no es una fecha valida."""
    if not valor:
        return None
    try:
        return datetime.strptime(str(valor).strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def formatear_fecha(valor: date | None) -> str:
    return valor.isoformat() if valor else ""


# --- Clasificacion: sin politica dentro ---------------------------------------


def clasificar_modalidad(texto: str) -> str:
    """Dato observado en la oferta, sin opinion.

    Devuelve REMOTO, HIBRIDO, PRESENCIAL o UNKNOWN.

    UNKNOWN es un resultado honesto y frecuente. Importante: UNKNOWN NO es
    REMOTO. No encontrar la palabra "presencial" no significa que el puesto sea
    remoto; significa que la oferta no lo dice, y ese es un dato distinto.
    """
    t = normalizar(texto)
    if not t:
        return "UNKNOWN"

    # La barra se normaliza para que "on-site" y "on site" count igual.
    t = t.replace("-", " ")

    hibrido = any(p in t for p in ("hibrid", "mixto"))
    remoto = any(p in t for p in ("teletrabajo", "remoto", "remote", "home office"))
    presencial = any(p in t for p in ("presencial", "on site", "onsite", "en oficina"))

    if hibrido:
        return "HIBRIDO"

    # Si el texto menciona las dos cosas sin decir "hibrido", casi siempre es un
    # puesto mixto. Se resuelve a favor de HIBRIDO: es la lectura que menos
    # descarta ofertas, y una ambiguedad no debe convertirse en un filtro.
    if remoto and presencial:
        return "HIBRIDO"

    if remoto:
        return "REMOTO"
    if presencial:
        return "PRESENCIAL"
    return "UNKNOWN"


def clasificar_contrato(texto: str) -> str:
    """Dato observado en la oferta, sin opinion.

    Devuelve TEMPORAL, INDEFINIDO, PRACTICAS o UNKNOWN.

    "Se valoran practicas" significa que las practicas son un plus, no que el
    puesto sea de practicas. Por eso se comprueba primero la mencion de un
    puesto de practicas, y no la palabra suelta.
    """
    t = normalizar(texto)
    if not t:
        return "UNKNOWN"

    # Orden importante: primero lo que identifica un puesto de practicas.
    if "puesto de practicas" in t or "becario" in t or "beca" in t:
        return "PRACTICAS"
    if "indefinido" in t:
        return "INDEFINIDO"
    if "temporal" in t or "fijo-discontinuo" in t:
        return "TEMPORAL"
    if "autonomo" in t:
        return "AUTONOMO"

    # "se valoran practicas", "valorable tener practicas": el puesto NO es de
    # practicas y la oferta no dice nada del contrato. UNKNOWN, no PRACTICAS.
    return "UNKNOWN"
