#!/usr/bin/env python3
"""Convierte un CSV suelto de ofertas en filas de pipeline.

Util para cuando tienes ofertas guardadas en otro sitio (un export del portal,
una hoja de calculo) y las quieres incorporar al pipeline de golpe.

Reglas de seguridad:
  - Nunca modifica filas existentes. Solo anade.
  - Detecta duplicados por URL antes de insertar.
  - Backup rotativo antes de escribir.
  - Los valores que no se pueden determinar se dejan como UNKNOWN.

Uso:
    python 4-ofertas/scripts/importar-ofertas.py ofertas.csv
    python 4-ofertas/scripts/importar-ofertas.py ofertas.csv --columnas titulo:Texto,empresa:Texto
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utilidades import (  # noqa: E402
    PipelineError,
    escribir_pipeline,
    generar_id,
    leer_pipeline,
    ruta_pipeline,
)

# Columnas de destino y de donde se leen en el CSV de entrada.
MAPEO = {
    "Empresa": "empresa",
    "Puesto": "titulo",
    "Ubicacion": "ubicacion",
    "Modalidad": "modalidad",
    "Contrato": "contrato",
    "Salario": "salario",
    "Fuente": "fuente",
    "URL": "url",
    "Contacto": "contacto",
    "Notas": "notas",
}

NO_DETERMINADO = "UNKNOWN"


def cargar_modulo(nombre: str, ruta: Path):
    """Carga un script con guion en el nombre (import normal no puede)."""
    spec = importlib.util.spec_from_file_location(nombre.replace("-", "_"), ruta)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(modulo)
    return modulo


def detectar_columnas(cabecera: list[str], especificacion: str | None) -> dict[str, str]:
    """Mapea columnas de destino a columnas de entrada.

    Sin especificacion, se emparejan por nombre en minusculas. Con ella, el
    formato es destino:entrada.
    """
    if especificacion:
        mapeo = {}
        for par in especificacion.split(","):
            if ":" not in par:
                raise PipelineError(f"Formato invalido en --columnas: {par!r}. Usa destino:entrada")
            destino, entrada = par.split(":", 1)
            mapeo[destino.strip()] = entrada.strip()
        return mapeo

    minusculas = {c.strip().lower(): c for c in cabecera}
    return {
        destino: minusculas[entrada]
        for destino, entrada in MAPEO.items()
        if entrada in minusculas
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Importa ofertas de un CSV al pipeline")
    ap.add_argument("origen", type=Path, help="CSV de entrada")
    ap.add_argument("--pipeline", type=Path, default=None)
    ap.add_argument("--columnas", default=None,
                    help="Mapeo destino:entrada, separado por comas")
    ap.add_argument("--estado", default="Detectada")
    ap.add_argument("--dry-run", action="store_true", help="No escribe nada")
    args = ap.parse_args()

    if not args.origen.exists():
        print(f"ERROR: no existe {args.origen}", file=sys.stderr)
        return 1

    ruta = args.pipeline or ruta_pipeline()
    agregar = cargar_modulo("agregar-oferta", Path(__file__).parent / "agregar-oferta.py")

    with args.origen.open(newline="", encoding="utf-8-sig") as fh:
        lector = csv.DictReader(fh)
        if not lector.fieldnames:
            print("ERROR: el CSV no tiene cabecera", file=sys.stderr)
            return 1
        mapeo = detectar_columnas(lector.fieldnames, args.columnas)
        entrada = list(lector)

    if not mapeo:
        print("ERROR: no se ha podido mapear ninguna columna.", file=sys.stderr)
        print(f"       Cabecera detectada: {', '.join(lector.fieldnames)}", file=sys.stderr)
        print("       Usa --columnas destino:entrada", file=sys.stderr)
        return 1

    try:
        filas = leer_pipeline(ruta)
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    hoy = date.today()
    anadidas = 0
    duplicadas = 0
    incompletas = 0

    for registro in entrada:
        valores = {destino: (registro.get(origen) or "").strip()
                   for destino, origen in mapeo.items()}

        empresa = valores.get("Empresa", "")
        puesto = valores.get("Puesto", "")
        if not empresa or not puesto:
            incompletas += 1
            continue

        url = valores.get("URL", "")
        if agregar.buscar_duplicado(filas, url):
            duplicadas += 1
            continue

        modalidad = valores.get("Modalidad") or NO_DETERMINADO
        contrato = valores.get("Contrato") or NO_DETERMINADO

        filas.append({
            "ID": generar_id(empresa, puesto, hoy),
            "Fecha": hoy.isoformat(),
            "Empresa": empresa,
            "Puesto": puesto,
            "Ubicacion": valores.get("Ubicacion", ""),
            "Modalidad": modalidad,
            "Contrato": contrato,
            "Salario": valores.get("Salario", ""),
            "Fuente": valores.get("Fuente", "Importado"),
            "URL": url,
            "Estado": args.estado,
            "Contacto": valores.get("Contacto", ""),
            "ProximaAccion": "",
            "FechaSeguimiento": "",
            "Encaje": "",
            "Notas": valores.get("Notas", "").replace(",", ";"),
        })
        anadidas += 1

    print(f"Leidas:    {len(entrada)}")
    print(f"Anadidas:  {anadidas}")
    print(f"Duplicadas (misma URL): {duplicadas}")
    print(f"Incompletas (sin empresa o puesto): {incompletas}")

    if args.dry_run:
        print("\n--dry-run: no se ha escrito nada.")
        return 0

    if anadidas:
        backup = escribir_pipeline(ruta, filas)
        print(f"\nEscritas {anadidas} filas en {ruta.name}")
        if backup:
            print(f"Backup: {backup.name}")
    else:
        print("\nNada que escribir.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
