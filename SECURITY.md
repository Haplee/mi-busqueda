# Security

## Supported versions

Solo la rama `main` recibe correcciones. Este repo es una plantilla de uso personal:
no hay versiones publicadas ni un ciclo de soporte que mantener.

| Versión | Soportada |
|---------|-----------|
| `main` | Sí |
| Ramas antiguas | No |

## Reportar un problema

No abras un issue público para un fallo de seguridad. Usa el aviso privado de
GitHub: **Security** → **Report a vulnerability**.

O abre un issue en privado si lo prefieres, describiendo solo lo necesario.

## Qué cuenta como fallo de seguridad aquí

Este repo no tiene servidor, ni base de datos, ni despliegue. Es HTML, Markdown y
Python. Por eso el modelo de amenaza es concreto y pequeño:

| Problema | Por qué importa |
|----------|-----------------|
| Fuga de datos personales | Es el riesgo principal. Ver `PRIVACY.md` |
| Falsos negativos en `check-privacidad.py` | Un email o un teléfono que pasa el escáner y acaba en un commit público |
| Un script que escribe fuera de su repo | Los scripts declaran no tocar nada fuera de la máquina del usuario |
| Un script que accede a la red | Ninguno lo hace, y debe seguir siendo así |
| Modificación de filas en estado protegido | El pipeline es un registro histórico de lo que pasó de verdad |

## Superficie de ataque

- **Los scripts.** Se ejecutan en la máquina de quien los clona, con sus permisos.
- **Los hooks de git.** `pre-commit` y el workflow de GitHub Actions ejecutan código.
- **Las dependencias.** Ninguna en tiempo de ejecución; `pytest` solo para los tests.
- **El contenido del repo.** Markdown y ficheros de texto. Nada se renderiza como HTML.

## Reglas de los scripts

Todo script nuevo debe cumplir esto:

1. **Rutas relativas.** `Path(__file__).resolve().parents[N]`. Nunca una ruta absoluta de una máquina.
2. **Sin red.** Ni `requests`, ni `urllib`, ni abrir un navegador. Si alguna vez hace falta una API, se documenta aquí antes de existir.
3. **Sin credenciales.** No se leen variables de entorno con secretos, ni se leen ficheros de usuario fuera del repo.
4. **Escrituras controladas.** Solo `pipeline.csv`, siempre vía `escribir_pipeline()`, que comprueba los estados protegidos antes de crear el backup.
5. **Sin preferencias personales en el código.** Van en `config.toml`.
6. **Con test.** En `4-ofertas/tests/`.

## Sobre el scraping

No está en el repo, y no se va a añadir.

Automatizar el acceso a portales de empleo choca con los términos de uso de
casi todos ellos, incluidos los que lo ofrecen como API "para uso personal". Donde
existe una API y se respetan sus límites, úsala por separado y con tu propia
autenticación. Este repo se queda con lo que sí puedes automatizar sin riesgo:
tus propios ficheros.

Y el login con tu cuenta de LinkedIn queda fuera por completo. Automatizarlo
expone tu cuenta y es una vía directa a que la bloqueen, y no gana nada a cambio.

## Divulgación

Sin ventana de undisclosed. Se corrige y se publica. Es un repo pequeño sin
infraestructura: no hay nada que contener antes de arreglarlo.
