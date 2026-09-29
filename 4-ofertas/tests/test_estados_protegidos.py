"""Los estados protegidos no se tocan. Nunca.

Estos tests son la garantia de que automatizar el pipeline no destruye el
historico. Si alguien anade una funcion que actualice filas, tiene que pasar
por aqui o el test falla.
"""

from __future__ import annotations

import pytest

from utilidades import (
    ALIAS_ESTADOS,
    ESTADO_EJEMPLO,
    ESTADOS,
    ESTADOS_PROTEGIDOS,
    EstadoProtegidoError,
    leer_pipeline,
)


class TestDefinicionDeEstados:
    def test_los_protegidos_estan_en_la_lista_de_estados(self):
        assert ESTADOS_PROTEGIDOS <= set(ESTADOS)

    def test_los_cinco_protegidos(self):
        assert ESTADOS_PROTEGIDOS == {
            "Enviada",
            "Seguimiento",
            "Entrevista",
            "PruebaTecnica",
            "Oferta",
        }

    def test_estados_preparacion_no_estan_protegidos(self):
        """Los de preparacion si se pueden tocar: aun no has enviado nada."""
        for estado in ("Detectada", "Revisada", "Interesante", "Ajustada"):
            assert estado not in ESTADOS_PROTEGIDOS

    def test_estados_terminales_no_estan_protegidos(self):
        """Rechazada, Descartada y SinRespuesta son finales: actualizarlas es correcto."""
        for estado in ("Rechazada", "Descartada", "SinRespuesta"):
            assert estado not in ESTADOS_PROTEGIDOS

    def test_prueba_tecnicasin_acentos(self):
        """El pipeline es un CSV. Un acento de mas es un estado que no coincide."""
        assert all(estado.isascii() for estado in ESTADOS)

    def test_los_alias_de_prueba_tecnicanormalizan(self):
        """Un pipeline escrito a mano puede traer 'Prueba Técnica' o 'Prueba'."""
        for variante in ("Prueba Técnica", "Prueba", "prueba técnica"):
            assert ALIAS_ESTADOS[variante] == "PruebaTecnica"


class TestEstadosProtegidosEnElCsv:
    def test_filas_protegidas_se_leen_correctamente(self, pipeline_csv):
        filas = leer_pipeline(pipeline_csv)
        protegidas = [f for f in filas if f["Estado"] in ESTADOS_PROTEGIDOS]
        assert len(protegidas) == 3  # Enviada, Entrevista, Oferta

    def test_leer_no_modifica_el_fichero(self, pipeline_csv):
        """Un script de solo lectura no puede cambiar ni un byte."""
        antes = pipeline_csv.read_bytes()
        leer_pipeline(pipeline_csv)
        assert pipeline_csv.read_bytes() == antes

    def test_leer_normaliza_el_estado_sin_tocar_el_csv(self, pipeline_csv):
        """'Prueba Técnica' se lee como 'PruebaTecnica', pero el fichero no cambia."""
        import csv

        filas = leer_pipeline(pipeline_csv)
        filas[0]["Estado"] = "Prueba Técnica"
        with pipeline_csv.open("w", newline="", encoding="utf-8") as fh:
            escritor = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
            escritor.writeheader()
            escritor.writerows(filas)

        assert leer_pipeline(pipeline_csv)[0]["Estado"] == "PruebaTecnica"
        assert b"Prueba T\xc3\xa9cnica" in pipeline_csv.read_bytes()


class TestProteccionEnEscritura:
    def test_escribir_crea_backup_antes(self, pipeline_csv):
        """Toda escritura pasa por crear backup antes de tocar el original."""
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        backup = escribir_pipeline(pipeline_csv, filas)

        assert backup is not None
        assert backup.exists()
        assert backup.name == "pipeline.csv.bak"

    def test_backup_contiene_el_estado_anterior(self, pipeline_csv):
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        filas[0]["Estado"] = "Descartada"
        escribir_pipeline(pipeline_csv, filas)

        # El backup debe seguir teniendo el estado original.
        from utilidades import ruta_backup

        originales = leer_pipeline(ruta_backup(pipeline_csv))
        assert originales[0]["Estado"] == "Detectada"

    def test_no_se_puede_cambiar_el_estado_de_una_fila_enviada(self, pipeline_csv):
        """El caso central: pasar 'Enviada' a 'Descartada' rompe el historico."""
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        enviadas = [f for f in filas if f["Estado"] == "Enviada"]
        enviadas[0]["Estado"] = "Descartada"

        with pytest.raises(EstadoProtegidoError, match="Enviada"):
            escribir_pipeline(pipeline_csv, filas)

    def test_no_se_puede_cambiar_cualquier_campo_de_una_fila_enviada(self, pipeline_csv):
        """No es solo el estado. Tambien el salario, la fecha o las notas."""
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        enviadas = [f for f in filas if f["Estado"] == "Enviada"]
        enviadas[0]["Salario"] = "999999"

        with pytest.raises(EstadoProtegidoError, match="Salario"):
            escribir_pipeline(pipeline_csv, filas)

    def test_no_se_puede_eliminar_una_fila_enviada(self, pipeline_csv):
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        filas = [f for f in filas if f["Estado"] != "Enviada"]

        with pytest.raises(EstadoProtegidoError, match="eliminada"):
            escribir_pipeline(pipeline_csv, filas)

    def test_no_se_puede_avanzar_de_una_fila_enviada_a_otro_protegido(self, pipeline_csv):
        """Avanzar de Enviada a Entrevista es legitimo... a mano, no por script."""
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        enviadas = [f for f in filas if f["Estado"] == "Enviada"]
        enviadas[0]["Estado"] = "Entrevista"

        with pytest.raises(EstadoProtegidoError):
            escribir_pipeline(pipeline_csv, filas)

    def test_la_escritura_fallida_no_toca_el_csv(self, pipeline_csv):
        """Si la comprobacion falla, el pipeline tiene que seguir igual."""
        from utilidades import escribir_pipeline

        antes = pipeline_csv.read_bytes()
        filas = leer_pipeline(pipeline_csv)
        [f for f in filas if f["Estado"] == "Enviada"][0]["Estado"] = "Descartada"

        with pytest.raises(EstadoProtegidoError):
            escribir_pipeline(pipeline_csv, filas)

        assert pipeline_csv.read_bytes() == antes

    def test_si_una_fila_no_protegida_cambia_no_falla(self, pipeline_csv):
        """Las filas de preparacion se pueden tocar: para eso son el filtro."""
        from utilidades import escribir_pipeline

        filas = leer_pipeline(pipeline_csv)
        detectadas = [f for f in filas if f["Estado"] == "Detectada"]
        detectadas[0]["Estado"] = "Descartada"
        detectadas[0]["Encaje"] = "3"

        escribir_pipeline(pipeline_csv, filas)

        assert leer_pipeline(pipeline_csv)[0]["Estado"] == "Descartada"

    def test_anadir_filas_no_toca_las_existentes(self, pipeline_csv, fila):
        """El caso normal de agregar-oferta: solo crece el pipeline."""
        from utilidades import escribir_pipeline, generar_id

        filas = leer_pipeline(pipeline_csv)
        filas.append(fila(ID=generar_id("Empresa Nueva", "Puesto Nuevo")))
        escribir_pipeline(pipeline_csv, filas)

        assert len(leer_pipeline(pipeline_csv)) == len(filas)

    def test_añadir_en_ingles_no_duplica_la_prueba(self):
        """'Prueba Tecnica' sin tilde tambien vale. Una sola fila, no dos."""
        from utilidades import (
            EstadoProtegidoError as Error,
            comprobar_protegidas,
        )

        antes = [{"ID": "F-1", "Estado": "PruebaTecnica"}]
        despues = [{"ID": "F-1", "Estado": "Prueba Técnica"}]

        with pytest.raises(Error):
            comprobar_protegidas(antes, despues)


class TestFiltroDeEjemplos:
    """Una fila de ejemplo no es una candidatura y no cuenta como tal."""

    def test_estado_ejemplo_no_esta_en_la_lista_de_estados_reales(self):
        assert ESTADO_EJEMPLO not in ESTADOS

    def test_fila_ejemplo_no_es_protegida(self):
        assert ESTADO_EJEMPLO not in ESTADOS_PROTEGIDOS

    def test_filas_reales_excluye_ejemplos(self, pipeline_csv, config_prueba):
        import importlib

        filas_reales = importlib.import_module("ver-ofertas").filas_reales

        filas = leer_pipeline(pipeline_csv)
        reales = filas_reales(filas, config_prueba)

        assert len(reales) == 5
        assert all(f["Estado"] != ESTADO_EJEMPLO for f in reales)
        assert all(f["Notas"] != "fila de demostracion" for f in reales)
