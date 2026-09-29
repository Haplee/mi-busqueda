"""El clasificador dice lo que ve, sin decidir nada.

Estos tests existen para proteger la regla que mas errores causa cuando se
incumple:

    UNKNOWN no es REMOTO.

Si no encuentras la palabra "presencial", el puesto puede ser remoto,
presencial, o no dizerlo. Convertir UNKNOWN en REMOTO es inventar un dato, y
los datos inventados acaban tomando decisiones de filtro.
"""

from __future__ import annotations

import pytest

from utilidades import clasificar_contrato, clasificar_modalidad, normalizar


class TestNormalizar:
    @pytest.mark.parametrize(
        "entrada,esperado",
        [
            ("Madrid", "madrid"),
            ("MADRID", "madrid"),
            ("Cádiz", "cadiz"),
            ("Málaga", "malaga"),
            ("A Coruña", "a coruna"),
            ("  Con  espacios  ", "con espacios"),
            ("Híbrido", "hibrido"),
            ("Nivel 3", "nivel 3"),
            ("", ""),
            (None, ""),
        ],
    )
    def test_normaliza_acentos_y_mayusculas(self, entrada, esperado):
        assert normalizar(entrada) == esperado

    def test_colapsa_guiones_bajos(self):
        assert normalizar("ADMIN_SISTEMAS  tecnico") == "admin sistemas tecnico"


class TestClasificarModalidad:
    @pytest.mark.parametrize(
        "texto",
        [
            "Trabajo 100% remoto desde casa",
            "Remote work, home office",
            "Ofrecemosremote",
            "teletrabajo",
        ],
    )
    def test_detecta_remoto(self, texto):
        assert clasificar_modalidad(texto) == "REMOTO"

    @pytest.mark.parametrize(
        "texto",
        [
            "Modalidad híbrida: 2 días en oficina",
            "Mixto presencial y remoto",
            "Híbrido flexible",
        ],
    )
    def test_detecta_hibrido(self, texto):
        assert clasificar_modalidad(texto) == "HIBRIDO"

    @pytest.mark.parametrize(
        "texto",
        [
            "Presencial en Madrid",
            "Trabajo on-site",
            "100% presencial en oficina de Barcelona",
        ],
    )
    def test_detecta_presencial(self, texto):
        assert clasificar_modalidad(texto) == "PRESENCIAL"

    @pytest.mark.parametrize(
        "texto",
        [
            "",
            "Ofrecemos puesto de soporte",
            "Se busca técnico con experiencia en redes",
            "Sin modalidad indicada",
            "Trabaja con nosotros",
        ],
    )
    def test_desconocido_no_es_remoto(self, texto):
        """El caso que mas falla en la practica."""
        assert clasificar_modalidad(texto) == "UNKNOWN"

    def test_hibrido_tiene_prioridad_sobre_remoto(self):
        """Un texto que menciona hibrido es HIBRIDO, aunque tambien diga remoto."""
        texto = "Trabajo híbrido, con posibilidad de remoto"
        assert clasificar_modalidad(texto) == "HIBRIDO"

    def test_presencial_y_remoto_sin_hibrido_es_hibrido(self):
        """Mencionar las dos cosas sin decir "hibrido" casi siempre es mixto.

        Es el caso ambiguo por definicion. HIBRIDO es la lectura que menos
        descarta ofertas: convertir la ambiguedad en un filtro estrecho seria
        repetir el error que UNUNKNOWN evita.
        """
        texto = "Presencial en oficina, aunque el equipo es remoto"
        assert clasificar_modalidad(texto) == "HIBRIDO"

    def test_guion_no_parte_la_palabra(self):
        assert clasificar_modalidad("Trabajo on-site en Madrid") == "PRESENCIAL"


class TestClasificarContrato:
    @pytest.mark.parametrize(
        "texto",
        [
            "Contrato indefinido",
            "Contrato estable, indefinido",
            "Contrato INDEFINIDO con continuidad",
        ],
    )
    def test_detecta_indefinido(self, texto):
        assert clasificar_contrato(texto) == "INDEFINIDO"

    def test_detecta_temporal(self):
        assert clasificar_contrato("Contrato temporal de 6 meses") == "TEMPORAL"

    def test_detecta_autonomo(self):
        assert clasificar_contrato("Trabajo como autónomo") == "AUTONOMO"

    def test_detecta_puesto_de_practicas(self):
        texto = "Puesto de prácticas en departamento de sistemas"
        assert clasificar_contrato(texto) == "PRACTICAS"

    def test_practicas_valoradas_no_es_puesto_de_practicas(self):
        """El caso trampa: "se valoran practicas" NO es un puesto de practicas."""
        texto = "Tecnico de soporte. Se valoran practicas de master."
        assert clasificar_contrato(texto) == "UNKNOWN"

    def test_beca_es_practicas(self):
        assert clasificar_contrato("Beca de colaboración en sistemas") == "PRACTICAS"

    def test_indefinido_gana_a_practicas_valoradas(self):
        texto = "Contrato indefinido. Se valoran prácticas."
        assert clasificar_contrato(texto) == "INDEFINIDO"

    @pytest.mark.parametrize("texto", ["", "Ofrecemos puesto", "Sin condiciones"])
    def test_desconocido(self, texto):
        assert clasificar_contrato(texto) == "UNKNOWN"


class TestSeparacionParserPolitica:
    """El parser dice lo que ve; la politica vive en config.toml."""

    def test_parser_no_consulta_config(self):
        import inspect

        fuente = inspect.getsource(clasificar_modalidad) + inspect.getsource(
            clasificar_contrato
        )
        for prohibido in ("config", "preferencia", "config.toml"):
            assert prohibido not in fuente.lower(), (
                f"El parser menciona {prohibido!r}: la politica debe vivir en config.toml"
            )
