"""Duplicados, backups rotativos y rutas portables.

Tres cosas que, si fallan, hacen que el repo no sirva en el ordenador de
otra persona o que acabe con 300 ficheros .bak acumulados.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from utilidades import (
    generar_id,
    leer_pipeline,
    ruta_backup,
    ruta_ejemplo,
    ruta_pipeline,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestDuplicados:
    """importlib y no import normal: el fichero se llama agregar-oferta.py."""

    @staticmethod
    def mod():
        import importlib

        return importlib.import_module("agregar-oferta")

    def test_misma_url_con_query_distinta_es_duplicado(self):
        mod = self.mod()
        filas = [{"URL": "https://example.com/empleo/1?utm_source=alert"}]
        assert mod.normalizar_url(filas[0]["URL"]) == "https://example.com/empleo/1"
        assert mod.buscar_duplicado(filas, "https://example.com/empleo/1") is not None

    def test_url_con_barra_final_es_duplicado(self):
        mod = self.mod()
        assert mod.normalizar_url("https://example.com/empleo/1/") == "https://example.com/empleo/1"
        filas = [{"URL": "https://example.com/empleo/1"}]
        assert mod.buscar_duplicado(filas, "https://example.com/empleo/1/") is not None

    def test_urls_distintas_no_son_duplicados(self):
        mod = self.mod()
        filas = [{"URL": "https://example.com/empleo/1"}]
        assert mod.buscar_duplicado(filas, "https://example.com/empleo/2") is None

    def test_fila_sin_url_no_genera_falsos_duplicados(self):
        mod = self.mod()
        filas = [{"URL": ""}, {"URL": ""}]
        assert mod.buscar_duplicado(filas, "") is None

    def test_id_unico_para_empresas_distintas(self):
        from datetime import date

        dia = date(2026, 1, 15)
        assert generar_id("Empresa Uno", "Puesto", dia) != generar_id(
            "Empresa Dos", "Puesto", dia
        )

    def test_id_es_legible(self):
        from datetime import date

        id_ = generar_id("Empresa Ficticia S.L.", "Técnico de Soporte", date(2026, 1, 15))
        assert id_ == "2026-01-15_empresa-ficticia-s-l_tecnico-de-soporte"


class TestBackupRotativo:
    def test_ruta_de_backup(self, pipeline_csv):
        assert ruta_backup(pipeline_csv).name == "pipeline.csv.bak"

    def test_no_se_generan_backups_con_fecha(self, pipeline_csv):
        """El patron pipeline.csv.bak-AAAAMMDD-HHMMSS genera cientos de ficheros."""
        assert not re.search(r"\.bak[-_]\d", ruta_backup(pipeline_csv).name)

    def test_solo_existe_un_backup_tras_varias_ejecuciones(self, pipeline_csv):
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        for i in range(5):
            filas[0]["Notas"] = f"ejecucion {i}"
            escribir_pipeline(pipeline_csv, filas)

        backups = list(pipeline_csv.parent.glob("pipeline.csv.bak*"))
        assert len(backups) == 1

    def test_backup_se_sobrescribe(self, pipeline_csv):
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        filas[0]["Notas"] = "primera"
        escribir_pipeline(pipeline_csv, filas)

        filas[0]["Notas"] = "segunda"
        escribir_pipeline(pipeline_csv, filas)

        assert len(list(pipeline_csv.parent.glob("pipeline.csv.bak*"))) == 1
        assert leer_pipeline(ruta_backup(pipeline_csv))[0]["Notas"] == "primera"


class TestRutasPortables:
    """Ningun script puede depender de donde este el repo en el disco."""

    PATRONES_PROHIBIDOS = (
        r"C:\\Users",
        r"/home/[a-z]",
        r"/Users/[A-Za-z]",
        r"AppData",
        r"Desktop\\PC",
        r"C:\\Program Files",
    )

    def scripts(self) -> list[Path]:
        return sorted((REPO_ROOT / "4-ofertas" / "scripts").glob("*.py"))

    def test_hay_scripts_que_analizar(self):
        assert len(self.scripts()) >= 3

    @pytest.mark.parametrize("patron", PATRONES_PROHIBIDOS)
    def test_ningun_script_tiene_rutas_absolutas_de_usuario(self, patron):
        for script in self.scripts():
            contenido = script.read_text(encoding="utf-8")
            assert not re.search(patron, contenido, re.IGNORECASE), (
                f"{script.name} contiene una ruta personal: {patron}"
            )

    def test_rutas_se_resuelven_desde_el_repo(self):
        """Las rutas se derivan de la ubicacion del fichero, no del CWD."""
        assert ruta_pipeline().parent.name == "4-ofertas"
        assert ruta_ejemplo().name == "pipeline.example.csv"
        assert REPO_ROOT in ruta_pipeline().parents

    def test_el_repo_funciona_desde_otro_directorio(self, tmp_path):
        """Ejecutar el script desde otro sitio no debe cambiar el resultado.

        Se ejecuta con --pipeline apuntando a un CSV temporal, para comprobar
        que el script localiza el repo por su propia ubicacion y no por el
        directorio de trabajo.
        """
        pipeline = tmp_path / "pipeline.csv"
        pipeline.write_text(
            "ID,Fecha,Empresa,Puesto,Ubicacion,Modalidad,Contrato,Salario,Fuente,URL,"
            "Estado,Contacto,ProximaAccion,FechaSeguimiento,Encaje,Notas\n"
            "F-1,2026-01-15,Empresa Ficticia,Tecnico,Ciudad,Remoto,Indefinido,,Portal,"
            "https://example.com/1,Interesante,,,,8,\n",
            encoding="utf-8",
        )

        script = REPO_ROOT / "4-ofertas" / "scripts" / "ver-ofertas.py"
        resultado = subprocess.run(
            [sys.executable, str(script), "--pipeline", str(pipeline)],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert resultado.returncode == 0, resultado.stderr
        assert "Empresa Ficticia" in resultado.stdout


class TestPipelineEjemplo:
    """Lo unico que hay en git es el ejemplo: cabecera + filas EJEMPLO."""

    def test_el_ejemplo_existe(self):
        assert ruta_ejemplo().exists()

    def test_solo_tiene_cabecera_y_filas_de_ejemplo(self):
        filas = leer_pipeline(ruta_ejemplo())
        assert len(filas) == 2
        for fila in filas:
            assert fila["Estado"] == "EJEMPLO"

    def test_ninguna_fila_tiene_url_real(self):
        for fila in leer_pipeline(ruta_ejemplo()):
            assert fila["URL"].startswith("https://example.com/")

    def test_el_ejemplo_no_contamina_las_metricas(self):
        from utilidades import ESTADO_EJEMPLO

        filas = leer_pipeline(ruta_ejemplo())
        assert all(f["Estado"] == ESTADO_EJEMPLO for f in filas)


class TestScriptsReales:
    def test_py_compile_pasa(self):
        """Todos los scripts compilan."""
        for script in sorted((REPO_ROOT / "4-ofertas" / "scripts").glob("*.py")):
            resultado = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                capture_output=True,
                text=True,
            )
            assert resultado.returncode == 0, f"{script.name}: {resultado.stderr}"
