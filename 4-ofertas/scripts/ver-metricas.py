#!/usr/bin/env python3
"""Calcula metricas del funnel de forma automatica.

Solo LEE pipeline.csv. No modifica nada.

Las filas con Estado = EJEMPLO (configurable) se excluyen de todas las cifras:
una prueba o una demo no es una candidatura, y contarla falsea el diagnostico.

Uso:
    python 4-ofertas/scripts/ver-metricas.py
    python 4-ofertas/scripts/ver-metricas.py --pipeline otra/ruta.csv
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utilidades import (  # noqa: E402
    Config,
    PipelineError,
    leer_pipeline,
    parsear_fecha,
    ruta_pipeline,
)


def ratio(numerador: int, denominador: int) -> str:
    if not denominador:
        return "  -  "
    return f"{100 * numerador / denominador:5.1f}%"


def fecha_min(filas: list[dict], campo: str = "Fecha") -> str:
    fechas = [d for d in (parsear_fecha(f.get(campo, "")) for f in filas) if d]
    return min(fechas).isoformat() if fechas else "-"


def main() -> int:
    ap = argparse.ArgumentParser(description="Metricas del funnel (solo lectura)")
    ap.add_argument("--pipeline", type=Path, default=None)
    ap.add_argument("--desde", default="", help="AAAA-MM-DD, filtra por fecha")
    args = ap.parse_args()

    ruta = args.pipeline or ruta_pipeline()
    config = Config.cargar()

    try:
        todas = leer_pipeline(ruta)
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    ejemplos = [f for f in todas if f.get("Estado") in config.estados_ejemplo]
    filas = [f for f in todas if f.get("Estado") not in config.estados_ejemplo]

    desde = parsear_fecha(args.desde) if args.desde else None
    if desde:
        filas = [f for f in filas if (parsear_fecha(f.get("Fecha", "")) or desde) >= desde]

    if not filas:
        print("No hay ofertas reales en el pipeline.")
        if ejemplos:
            print(f"({len(ejemplos)} filas de ejemplo excluidas, correctamente)")
        return 0

    estados = Counter(f.get("Estado", "") for f in filas)
    enviadas = [f for f in filas if f.get("Estado") in
                ("Enviada", "Seguimiento", "Entrevista", "PruebaTecnica", "Oferta",
                 "SinRespuesta", "Rechazada")]
    detectadas = len(filas)
    respondieron = [f for f in enviadas if f.get("Estado") in
                    ("Entrevista", "PruebaTecnica", "Oferta", "Rechazada")]
    entrevistas = [f for f in filas
                   if f.get("Estado") in ("Entrevista", "PruebaTecnica", "Oferta")]
    pruebas = [f for f in filas if f.get("Estado") in ("PruebaTecnica", "Oferta")]
    ofertas = [f for f in filas if f.get("Estado") == "Oferta"]
    rechazos = [f for f in filas if f.get("Estado") == "Rechazada"]

    ancho = 68
    print("=" * ancho)
    print("METRICAS DEL FUNNEL".center(ancho))
    print("=" * ancho)
    print(f"Ofertas: {fecha_min(filas)} -> hoy")
    print()

    print("-- Volumen por estado " + "-" * (ancho - 22))
    for estado in sorted(estados, key=lambda e: -estados[e]):
        print(f"  {estado:<28} {estados[estado]:>5}")
    print()

    print("-- Embudo " + "-" * (ancho - 12))
    print(f"  {'Detectadas':<28} {detectadas:>5}")
    print(f"  {'Enviadas':<28} {len(enviadas):>5}")
    print(f"  {'Con respuesta':<28} {len(respondieron):>5}")
    print(f"  {'Entrevistas':<28} {len(entrevistas):>5}")
    print(f"  {'Pruebas tecnicas':<28} {len(pruebas):>5}")
    print(f"  {'Ofertas':<28} {len(ofertas):>5}")
    print(f"  {'Rechazos':<28} {len(rechazos):>5}")
    print()

    print("-- Ratios " + "-" * (ancho - 12))
    print(f"  {'detectada -> enviada':<28} {ratio(len(enviadas), detectadas)}")
    print(f"  {'enviada -> respuesta':<28} {ratio(len(respondieron), len(enviadas))}")
    print(f"  {'enviada -> entrevista':<28} {ratio(len(entrevistas), len(enviadas))}")
    print(f"  {'entrevista -> prueba':<28} {ratio(len(pruebas), len(entrevistas))}")
    print(f"  {'prueba -> oferta':<28} {ratio(len(ofertas), len(pruebas))}")
    print()

    print("-- Por portal " + "-" * (ancho - 15))
    totales = Counter(f.get("Fuente", "") or "Sin fuente" for f in filas)
    enviadas_por = Counter(f.get("Fuente", "") or "Sin fuente" for f in enviadas)
    print(f"  {'Portal':<24} {'Total':>7} {'Enviadas':>10} {'Tasa':>8}")
    for portal, total in totales.most_common():
        env = enviadas_por[portal]
        print(f"  {portal[:23]:<24} {total:>7} {env:>10} {ratio(env, total):>8}")
    print()

    print("-- Por modalidad " + "-" * (ancho - 18))
    por_mod = defaultdict(lambda: [0, 0])
    for f in filas:
        clave = f.get("Modalidad", "") or "Sin especificar"
        por_mod[clave][0] += 1
        if f in enviadas:
            por_mod[clave][1] += 1
    print(f"  {'Modalidad':<24} {'Total':>7} {'Enviadas':>10} {'Tasa':>8}")
    for modalidad, (total, env) in sorted(por_mod.items(), key=lambda kv: -kv[1][1]):
        print(f"  {modalidad[:23]:<24} {total:>7} {env:>10} {ratio(env, total):>8}")
    print()

    print("-- Por rango de encaje " + "-" * (ancho - 26))
    por_encaje = defaultdict(lambda: [0, 0])
    for f in filas:
        try:
            clave = min(10, max(1, int(f.get("Encaje", "") or 0))) or "sin puntuar"
        except ValueError:
            clave = "sin puntuar"
        por_encaje[str(clave)][0] += 1
        if f in enviadas:
            por_encaje[str(clave)][1] += 1
    print(f"  {'Encaje':<24} {'Total':>7} {'Enviadas':>10} {'Tasa':>8}")
    for encaje in sorted(por_encaje, key=lambda e: (len(e), e)):
        total, env = por_encaje[encaje]
        print(f"  {encaje:<24} {total:>7} {env:>10} {ratio(env, total):>8}")
    print()

    print("-- Avisos " + "-" * (ancho - 12))
    if ejemplos:
        print(f"  {len(ejemplos)} fila(s) de ejemplo excluidas de todas las cifras.")
    if len(enviadas) < 20:
        print(f"  Con {len(enviadas)} candidaturas, los ratios no son concluyentes.")
        print("  No cambies la estrategia hasta llegar a 20 o a 4 semanas.")
    sin_encaje = [f for f in filas if not f.get("Encaje")]
    if sin_encaje:
        print(f"  {len(sin_encaje)} ofertas sin encaje puntuado.")
    sin_seguimiento = [f for f in enviadas if not f.get("FechaSeguimiento")]
    if sin_seguimiento:
        print(f"  {len(sin_seguimiento)} enviadas sin fecha de seguimiento programada.")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
