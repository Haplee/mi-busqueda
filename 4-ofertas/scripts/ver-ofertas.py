#!/usr/bin/env python3
"""Revisa el pipeline y dice qué hay que hacer hoy.

Solo LEE. No modifica pipeline.csv en ningun caso.

Uso:
    python 4-ofertas/scripts/ver-ofertas.py
    python 4-ofertas/scripts/ver-ofertas.py --pipeline otra/ruta.csv
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utilidades import (  # noqa: E402
    Config,
    PipelineError,
    clasificar_modalidad,
    leer_pipeline,
    normalizar,
    parsear_fecha,
    ruta_pipeline,
)


def evaluar_config(fila: dict[str, str], config: Config) -> dict[str, object]:
    """Calcula el encaje por dimension. No decide nada: informa.

    Cada dimension se devuelve por separado a proposito. Un "8/10" unico
    esconde por que una oferta encaja o no, y eso es justo lo que hace
    imposible corregir los filtros.
    """
    texto = " ".join(
        fila.get(c, "") for c in ("Puesto", "Empresa", "Notas", "Ubicacion")
    ).lower()

    detalle: dict[str, object] = {}
    nota: list[str] = []

    # Rol
    if config.busqueda_keywords:
        normalizado = normalizar(texto)
        encontradas = [k for k in config.busqueda_keywords if normalizar(k) in normalizado]
        detalle["Rol"] = 10 if encontradas else 3
        if not encontradas:
            nota.append("ninguna palabra clave coincide")
    else:
        detalle["Rol"] = None  # config sin keywords: no se puede evaluar

    # Habilidades: cuenta cuantas de tus habilidades aparecen en la oferta
    habilidades = leer_habilidades()
    if habilidades:
        normalizado = normalizar(texto)
        halladas = [h for h in habilidades if normalizar(h) in normalizado]
        proporcion = len(halladas) / len(habilidades)
        detalle["Habilidades"] = round(10 * proporcion)
        detalle["_habilidades_halladas"] = halladas
    else:
        detalle["Habilidades"] = None

    # Ubicacion
    modalidad_fila = clasificar_modalidad(fila.get("Modalidad", ""))
    if config.modalidades:
        aceptadas = {normalizar(m) for m in config.modalidades}
        if modalidad_fila == "UNKNOWN":
            detalle["Ubicacion"] = 5
            nota.append("modalidad sin verificar")
        elif normalizar(modalidad_fila) in aceptadas:
            detalle["Ubicacion"] = 10
        else:
            detalle["Ubicacion"] = 2
            nota.append(f"modalidad {modalidad_fila} no esta en tus preferencias")
    else:
        detalle["Ubicacion"] = None

    # Contrato
    if config.contratos:
        normalizado = normalizar(fila.get("Contrato", ""))
        if not normalizado:
            detalle["Contrato"] = 5
            nota.append("contrato sin especificar")
        elif normalizado in {normalizar(c) for c in config.contratos}:
            detalle["Contrato"] = 10
        else:
            detalle["Contrato"] = 3
    else:
        detalle["Contrato"] = None

    # Seniority, deducido del titulo
    detalle["Seniority"] = detectar_seniority(fila.get("Puesto", ""))

    valores = [v for k, v in detalle.items() if not k.startswith("_") and v is not None]
    detalle["_encaje"] = round(sum(valores) / len(valores)) if valores else None
    detalle["_notas"] = nota

    return detalle


def leer_habilidades() -> list[str]:
    """Lee las habilidades del usuario desde 1-perfil-profesional/.

    Si el usuario no ha rellenado habilidades.md, devuelve [] y el script
    funciona igual: la dimension simplemente no se evalua.
    """
    ruta = Path(__file__).resolve().parents[2] / "1-perfil-profesional" / "habilidades.md"
    if not ruta.exists():
        return []
    encontradas: list[str] = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if not linea.startswith("|") or linea.count("|") < 3:
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        habilidad = celdas[0].strip("`* ")
        # Descarta cabeceras, separadores y marcadores de plantilla.
        if habilidad and not habilidad.startswith("-") and "[" not in habilidad:
            if not habilidad.lower().startswith(("habilidad", "nivel", "herramienta")):
                encontradas.append(habilidad)
    return encontradas


def detectar_seniority(puesto: str) -> int | None:
    t = normalizar(puesto)
    if not t:
        return None
    if "junior" in t or "entry" in t or "trainee" in t or "becario" in t:
        return 10
    if "senior" in t or "sr" in t.split() or "lead" in t or "principal" in t:
        return 3
    if "mid" in t:
        return 7
    return None


def filas_reales(filas: list[dict[str, str]], config: Config) -> list[dict[str, str]]:
    """Descarta las filas de ejemplo. No son candidaturas."""
    return [f for f in filas if f.get("Estado") not in config.estados_ejemplo]


def agrupar_por_accion(filas: list[dict[str, str]], hoy: date) -> dict[str, list]:
    grupos = {"hoy": [], "seguimiento": [], "sin_responder": [], "interesante": []}

    for fila in filas:
        estado = fila.get("Estado", "")

        if estado in ("Interesante", "Ajustada", "Revisada"):
            grupos["interesante"].append(fila)

        fecha_seguimiento = parsear_fecha(fila.get("FechaSeguimiento", ""))
        if fecha_seguimiento:
            if fecha_seguimiento <= hoy and estado not in (
                "Rechazada",
                "Descartada",
                "Oferta",
            ):
                grupos["seguimiento"].append(fila)
            elif fecha_seguimiento > hoy:
                dias = (fecha_seguimiento - hoy).days
                if dias <= 7:
                    grupos["hoy"].append(fila)

        if estado == "Enviada":
            enviada = parsear_fecha(fila.get("Fecha", ""))
            if enviada and hoy - enviada > timedelta(days=21):
                grupos["sin_responder"].append(fila)

    return grupos


def imprimir(grupos: dict[str, list], config: Config) -> None:
    titulos = {
        "hoy": "Seguimientos programados para hoy o esta semana",
        "seguimiento": "Seguimientos atrasados",
        "sin_responder": "Enviadas hace mas de 3 semanas sin movimiento",
        "interesante": "Ofertas marcadas como interesantes, sin preparar",
    }

    for clave in ("seguimiento", "hoy", "sin_responder", "interesante"):
        items = grupos[clave]
        print(f"\n{titulos[clave]} ({len(items)})")
        if not items:
            print("  -")
            continue
        for fila in items[:15]:
            encaje = evaluar_config(fila, config).get("_encaje")
            encaje_txt = f"{encaje}/10" if encaje is not None else "s/d"
            print(f"  {fila.get('Empresa', ''):<24} {fila.get('Puesto', '')[:38]:<38} {encaje_txt}")
            proxima = fila.get("ProximaAccion", "")
            if proxima:
                print(f"    -> {proxima}")
        if len(items) > 15:
            print(f"  ... y {len(items) - 15} mas")


def main() -> int:
    ap = argparse.ArgumentParser(description="Revisa el pipeline (solo lectura)")
    ap.add_argument("--pipeline", type=Path, default=None, help="Ruta alternativa")
    args = ap.parse_args()

    ruta = args.pipeline or ruta_pipeline()
    config = Config.cargar()

    try:
        filas = leer_pipeline(ruta)
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    reales = filas_reales(filas, config)
    ejemplos = len(filas) - len(reales)

    print(f"Pipeline: {ruta}")
    print(f"Ofertas: {len(reales)} reales, {ejemplos} de ejemplo (excluidas)")

    if not reales:
        print("\nNo hay ofertas en el pipeline. Copia pipeline.example.csv a pipeline.csv.")
        return 0

    if not config.busqueda_keywords:
        print(
            "\nAVISO: no hay keywords en config.toml, el encaje no se puede calcular.\n"
            "       Copia config.example.toml a config.toml y rellenalo."
        )

    imprimir(agrupar_por_accion(reales, date.today()), config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
