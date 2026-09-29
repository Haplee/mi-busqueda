#!/usr/bin/env python3
"""Añade una oferta al pipeline de forma segura.

Protecciones:
  - Crea backup rotativo antes de escribir.
  - No toca filas en estado protegido: solo añade filas nuevas.
  - Detecta duplicados por URL antes de insertar.

Uso:
    python 4-ofertas/scripts/agregar-oferta.py \
        --empresa "Nombre S.L." \
        --puesto "Tecnico de soporte" \
        --url "https://..." \
        --modalidad "Remoto" \
        --contrato "Indefinido" \
        --fuente "Portal" \
        --encaje 8
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
    escribir_pipeline,
    generar_id,
    leer_pipeline,
    ruta_pipeline,
)


def normalizar_url(url: str) -> str:
    """Compara URLs ignorando parametros de rastreo y barras finales."""
    if not url:
        return ""
    base = url.strip().split("?")[0].split("#")[0].rstrip("/")
    return base.lower()


def buscar_duplicado(filas: list[dict[str, str]], url: str) -> dict[str, str] | None:
    """Misma URL significa misma oferta, aunque el titulo haya cambiado."""
    objetivo = normalizar_url(url)
    if not objetivo:
        return None
    for fila in filas:
        if normalizar_url(fila.get("URL", "")) == objetivo:
            return fila
    return None


def inferir_modalidad(valor: str) -> str:
    """Si el usuario no dice nada, se clasifica el texto. Nunca se inventa.

    Lo que no se puede determinar queda como UNKNOWN, que es un dato honesto.
    """
    if valor.strip():
        return valor.strip()
    return "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser(description="Añade una oferta al pipeline")
    ap.add_argument("--empresa", required=True)
    ap.add_argument("--puesto", required=True)
    ap.add_argument("--url", default="")
    ap.add_argument("--ubicacion", default="")
    ap.add_argument("--modalidad", default="", help="Remoto, Hibrido, Presencial o texto libre")
    ap.add_argument("--contrato", default="")
    ap.add_argument("--salario", default="")
    ap.add_argument("--fuente", default="Manual")
    ap.add_argument("--contacto", default="")
    ap.add_argument("--estado", default="Detectada", help="Estado inicial")
    ap.add_argument("--encaje", type=int, default=None)
    ap.add_argument("--seguimiento-dias", type=int, default=None,
                    help="Dias hasta el seguimiento. Si se indica, programa la fecha.")
    ap.add_argument("--notas", default="")
    ap.add_argument("--pipeline", type=Path, default=None)
    args = ap.parse_args()

    ruta = args.pipeline or ruta_pipeline()
    config = Config.cargar()

    try:
        filas = leer_pipeline(ruta)
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    duplicado = buscar_duplicado(filas, args.url)
    if duplicado:
        print(f"La oferta ya existe en el pipeline: {duplicado['ID']}")
        print(f"  Estado actual: {duplicado['Estado']}")
        print("No se ha modificado nada.")
        return 1

    hoy = date.today()
    modalidad = inferir_modalidad(args.modalidad)
    # Si no se pasa --contrato, queda UNKNOWN. Nunca se infiere del titulo.
    contrato = args.contrato.strip() or "UNKNOWN"

    seguimiento = ""
    dias = args.seguimiento_dias
    if dias is None and args.estado in ("Enviada", "Seguimiento"):
        dias = 7
    if dias is not None:
        seguimiento = (hoy + timedelta(days=dias)).isoformat()

    nueva = {
        "ID": generar_id(args.empresa, args.puesto, hoy),
        "Fecha": hoy.isoformat(),
        "Empresa": args.empresa,
        "Puesto": args.puesto,
        "Ubicacion": args.ubicacion,
        "Modalidad": modalidad,
        "Contrato": contrato,
        "Salario": args.salario,
        "Fuente": args.fuente,
        "URL": args.url,
        "Estado": args.estado,
        "Contacto": args.contacto,
        "ProximaAccion": "",
        "FechaSeguimiento": seguimiento,
        "Encaje": str(args.encaje) if args.encaje is not None else "",
        "Notas": args.notas.replace(",", ";"),
    }

    filas.append(nueva)
    backup = escribir_pipeline(ruta, filas)

    print(f"Añadida: {nueva['ID']}")
    print(f"  Estado: {nueva['Estado']}")
    print(f"  Modalidad: {nueva['Modalidad']}")
    print(f"  Seguimiento: {seguimiento or 'no programado'}")
    if backup:
        print(f"  Backup: {backup.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
