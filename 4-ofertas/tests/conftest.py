"""Fixtures compartidas. Todos los datos son ficticios."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from utilidades import COLUMNAS  # noqa: E402


def nueva_fila(**kwargs) -> dict[str, str]:
    """Fila completa con valores por defecto, para no repetir 16 columnas.

    El nombre no es "fila" a proposito: un fixture llamado "fila" lo ocultaria
    en el scope del modulo, y escribirlo asi rompe todos los tests a la vez.
    """
    base = {c: "" for c in COLUMNAS}
    base.update(
        {
            "ID": "2026-01-15_Empresa_Puesto",
            "Fecha": "2026-01-15",
            "Empresa": "Empresa Ficticia",
            "Puesto": "Tecnico de Soporte",
            "Ubicacion": "Ciudad Inventada",
            "Modalidad": "Remoto",
            "Contrato": "Indefinido",
            "Salario": "",
            "Fuente": "Portal Ficticio",
            "URL": "https://example.com/empleo/1",
            "Estado": "Detectada",
            "Contacto": "",
            "ProximaAccion": "",
            "FechaSeguimiento": "",
            "Encaje": "8",
            "Notas": "",
        }
    )
    base.update({k: str(v) for k, v in kwargs.items()})
    return base


@pytest.fixture
def fila():
    """Constructor de filas, como fixture.

    Se llama "fila" porque es como lo piensa quien escribe el test:
    ``def test_x(self, fila)``.
    """
    return nueva_fila


@pytest.fixture
def pipeline_csv(tmp_path) -> Path:
    """Un pipeline.csv temporal con 6 filas ficticias."""
    import csv

    ruta = tmp_path / "pipeline.csv"
    filas = [
        nueva_fila(ID="F-001", Estado="Detectada", URL="https://example.com/empleo/1"),
        nueva_fila(ID="F-002", Estado="Interesante", URL="https://example.com/empleo/2", Encaje="9"),
        nueva_fila(ID="F-003", Estado="Enviada", Fecha="2025-10-01",
             URL="https://example.com/empleo/3", FechaSeguimiento="2026-01-20"),
        nueva_fila(ID="F-004", Estado="Entrevista", Fecha="2025-11-15",
             URL="https://example.com/empleo/4"),
        nueva_fila(ID="F-005", Estado="Oferta", Fecha="2025-12-01",
             URL="https://example.com/empleo/5", Encaje="10"),
        nueva_fila(ID="F-006", Estado="EJEMPLO", URL="https://example.com/ejemplo",
             Notas="fila de demostracion"),
    ]
    with ruta.open("w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=list(COLUMNAS))
        escritor.writeheader()
        escritor.writerows(filas)
    return ruta


@pytest.fixture
def config_prueba():
    """Config con preferencias ficticias, construida sin tocar ficheros."""
    from utilidades import Config

    return Config(
        busqueda_keywords=("tecnico", "soporte"),
        busqueda_exclude=("practicas",),
        modalidades=("Remoto",),
        contratos=("Indefinido", "Temporal"),
        salario_minimo=0,
        estados_ejemplo=frozenset({"EJEMPLO"}),
        palabras_prohibidas=(),
        umbral_interesante=7,
        fuentes_activas=(),
        path=None,
    )
