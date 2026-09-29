# AGENTS.md

Instrucciones para cualquier IA que trabaje en este repo. Lénelas antes de tocar
nada.

## Qué es este repo

Una plantilla de búsqueda de empleo. Documentos, un pipeline en CSV y cuatro
scripts locales. Nada más.

## Idioma

Todo el contenido, los nombres de variables, los comentarios y los mensajes de
error van en español. Los identificadores que cruzan una frontera (nombres de
columna del CSV) van en español también, para que no haya dos idiomas en el mismo
fichero.

## Las reglas que no se negocian

1. **No inventes experiencia.** Ni cifras, ni tecnologías, ni fechas, ni empresas.
   Si falta un dato, deja un marcador `[TU_...]` y sigue.
2. **No inventes fuentes.** Si no sabes algo de un framework o una librería, no lo
   escribas. `docs/primeros-pasos-con-ia.md` explica por qué.
3. **Nada de datos personales.** Ni de ejemplo. Usa marcadores entre corchetes.
4. **Nada de red en los scripts.** Ni `requests`, ni `urllib`, ni navegador.
5. **Nada de envío de candidaturas ni login.** Nunca. Ni siquiera "solo un ejemplo".
6. **Nunca escribas fuera del repo.** Ni en la carpeta del usuario, ni en
   `Documents`, ni en una ruta absoluta.
7. **Los estados protegidos no se tocan.** `Enviada`, `Seguimiento`,
   `Entrevista`, `PruebaTecnica`, `Oferta`. Ver `SECURITY.md`.

## Dónde está cada cosa

| Ruta | Contenido |
|------|-----------|
| `1-perfil-profesional/` | Fuente de verdad. Si algo no está aquí, no existe |
| `2-documentos/` | CV, carta, emails. Se generan desde el perfil |
| `3-presencia-online/` | LinkedIn, GitHub, portfolio |
| `4-ofertas/` | Pipeline y scripts |
| `5-postulaciones/` | Una carpeta por candidatura real. Ignorada por git |
| `6-entrevistas/` | Preparación y notas |
| `7-networking/` | Contactos y peticiones |
| `8-seguimiento/` | Qué toca y cuándo |
| `docs/` | Guías, incluida la de trabajo con IA |

## Cómo escribir un script

```python
# Bien: rutas relativas al repo
SCRIPTS_DIR = Path(__file__).resolve().parent
OFERTAS_DIR = SCRIPTS_DIR.parent

# Mal: ruta absoluta, dependiente de una maquina concreta
PIPELINE = Path("C:/TU_USUARIO/Escritorio/mi-carpeta/4-ofertas/pipeline.csv")

# Mal: asumir el directorio de trabajo
PIPELINE = Path("4-ofertas/pipeline.csv")
```

- Sin dependencias externas. `tomllib` y `csv` de la stdlib bastan.
- Preferencias en `config.toml`, nunca en el código.
- Si escribe, pasa por `escribir_pipeline()`: es el único punto de escritura.
- Si lee, no escribe nunca.
- Acompáñalo de un test en `4-ofertas/tests/`.
- Documéntalo en `4-ofertas/scripts/README.md`.

## `UNKNOWN` no es `REMOTO`

El clasificador devuelve `UNKNOWN` cuando la oferta no dice. Eso es un dato: la
oferta no lo especifica. No lo rellenes con una suposición. Un falso positivo
descarta ofertas que sí encajaban, y un falso negativo manda una candidatura a
destiempo.

Cuando un texto menciona "presencial" y "remoto" sin decir "híbrido", se resuelve
como `HIBRIDO`. Una ambigüedad no debe convertirse en un filtro.

## Convenciones

- Markdown con títulos en sentence case. Listas con `-`, tablas cuando hay dos o más
  dimensiones.
- Un bloque de código con su contenido o no es un bloque de código.
- Nada de emojis en el contenido del repo.
- Comentarios que explican **por qué**, no **qué**. Si el código ya lo dice, sobra.
- En español: "tú" con tuteo, "vale", "por favor". Sin regionalismos.
- Evita superlativos. "El mejor CV del mundo" no es un criterio, es ruido.
- Sin anglicismos innecesarios: "fecha de seguimiento", no "deadline".

## Antes de dar algo por terminado

```bash
python -m pytest 4-ofertas/tests/ -q
python scripts/check-privacidad.py --todo
```

Los dos tienen que pasar. El segundo importa más de lo que parece: este repo
existe para no filtrar datos.

Si has tocado un script, actualiza también
`4-ofertas/scripts/README.md`.
