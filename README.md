# mi-busqueda

Plantilla para llevar la búsqueda de empleo como se lleva un proyecto: con un
objetivo escrito, un perfil que se reutiliza, un pipeline de ofertas y un
seguimiento de lo que ya has enviado.

El CV no se guarda. Se genera desde `1-perfil-profesional/`, y todo lo demás
sale de ahí. Si el perfil está al día, actualizar el CV es editar cinco
ficheros de texto, no rehacer un documento.

```
0-objetivo  ->  1-perfil  ->  2-documentos  ->  3-presencia  ->  4-ofertas  ->  5-postulaciones
                                                                                          |
              8-seguimiento  <-  7-networking  <-  6-entrevistas  <------------------------+
```

## Qué te dice los scripts

`ver-ofertas.py` responde a la única pregunta que importa un martes por la
mañana: qué toca hoy.

```console
$ python 4-ofertas/scripts/ver-ofertas.py
Pipeline: 4-ofertas/pipeline.csv
Ofertas: 8 reales, 0 de ejemplo (excluidas)

Seguimientos atrasados (1)
  Nexora Consulting        Tecnico de soporte TI                  7/10  <- supera tu umbral
    -> Preparar STAR de outage

Seguimientos programados para hoy o esta semana (1)
  Vantage Tech             Tecnico de soporte                     6/10
    -> Reenviar recordatorio

Enviadas hace mas de 3 semanas sin movimiento (1)
  Empresa Aurora SL        Tecnico de soporte TI                  7/10  <- supera tu umbral
    -> Esperar respuesta

Pendientes de decidir (Interesante, Revisada, Ajustada) (2)
  Globex SA                Administrador de sistemas              6/10
    -> Descartar: presencial
  Korvus Data              Tecnico de datos                       4/10
    -> Revisar requisitos
```

El `7/10` sale de `evaluar_config()`: cinco dimensiones ponderadas según
`[scoring]` de `config.toml`, y cada una con su nota. El detalle importa más
que el total, porque un `4/10` puede ser "tecnología que no me gusta" o "puesto
que ni es lo mío".

`ver-metricas.py` convierte el historial en un funnel.

```console
$ python 4-ofertas/scripts/ver-metricas.py
-- Embudo --------------------------------------------------------
  Detectadas                       8
  Enviadas                         6
  Con respuesta                    4
  Entrevistas                      3
  Pruebas tecnicas                 2
  Ofertas                          1
  Rechazos                         1

-- Ratios --------------------------------------------------------
  detectada -> enviada          75.0%
  enviada -> respuesta          66.7%
  enviada -> entrevista         50.0%
  entrevista -> prueba          66.7%
  prueba -> oferta              50.0%

-- Por portal -----------------------------------------------------
  Portal                     Total   Enviadas     Tasa
  InfoJobs                       3          3   100.0%
  LinkedIn                       3          2    66.7%
  Portal de empleo               2          1    50.0%
```

Y avisa cuando las cifras no significan nada todavía:

```
-- Avisos --------------------------------------------------------
  Con 6 candidaturas, los ratios no son concluyentes.
  No cambies la estrategia hasta llegar a 20 o a 4 semanas.
  4 enviadas sin fecha de seguimiento programada.
```

Ese aviso es la parte que más cuesta. Es fácil tener 40 ofertas en el pipeline
y no sacar ninguna conclusión, porque los ratios con muestra pequeña siempre
parecen buenos.

## Empezar

```bash
git clone https://github.com/Haplee/mi-busqueda.git mi-busqueda
cd mi-busqueda
```

Tres ficheros, en este orden. El primero es el que más gente se salta.

```bash
# 1. Tus filtros
cp 4-ofertas/config.example.toml 4-ofertas/config.toml

# 2. Tu pipeline
cp 4-ofertas/pipeline.example.csv 4-ofertas/pipeline.csv
```

`config.toml` y `pipeline.csv` están en `.gitignore`. Son tuyos, y nunca se
suben. Los ficheros de texto se editan en el sitio, sin copias: si haces
`git diff` ves qué cambias.

### 1. El objetivo

`0-objetivo-y-estrategia/objetivo.md` es la parte que más impacto tiene y la
que más gente pospone. Cinco apartados: puesto objetivo, condiciones
aceptadas, restricciones reales, qué te hace atractivo al mercado, y salario
objetivo.

Un detalle que salva tiempo: el apartado de restricciones existe para que
descartes ofertas sin pensarlo. Si escribes ahí "presencial obligatoria en
Valencia", ya no tienes que releer cinco veces la misma oferta.

### 2. El perfil

Rellena `1-perfil-profesional/`. Es la fuente de verdad: si algo no está ahí,
no existe, aunque recuerdes haberlo hecho.

El orden importa. `banco-de-logros.md` va el primero de todos, porque es lo que
más cuesta y lo que más reutilizas: de ahí salen las líneas del CV, las
respuestas de entrevista y el titular del portfolio.

### 3. El pipeline

```bash
python 4-ofertas/scripts/agregar-oferta.py \
    --empresa "Nombre S.L." --puesto "Tecnico de soporte" \
    --url "https://..." --estado Detectada

# O de golpe, si ya tienes ofertas guardadas
python 4-ofertas/scripts/importar-ofertas.py ofertas.csv --dry-run
```

Always `--dry-run` primero al importar. Muestra qué añadiría y qué descarta
por duplicado, sin escribir nada.

## Estructura

| Carpeta | Qué vive ahí |
|---------|--------------|
| `0-objetivo-y-estrategia/` | Qué buscas, qué descartas y por qué |
| `1-perfil-profesional/` | Fuente de verdad. El CV sale de aquí |
| `2-documentos/` | CV, carta, correos |
| `3-presencia-online/` | GitHub, LinkedIn, portfolio |
| `4-ofertas/` | Pipeline en CSV, config y scripts |
| `5-postulaciones/` | Una carpeta por candidatura. Ignorada por git |
| `6-entrevistas/` | Preparación y qué preguntar |
| `7-networking/` | Contactos |
| `8-seguimiento/` | Registro y ratios de contacto |
| `9-recursos/` | Lecturas, comunidades, eventos |
| `examples/` | Perfil ficticio completo, de principio a fin |

El número del principio no es decorativo: es el orden en el que se rellena, y
la `1` va antes que la `2`.

## Scripts

Cuatro en `4-ofertas/scripts/`, todos locales, sin dependencias y sin red:

| Script | Para qué |
|--------|----------|
| `agregar-oferta.py` | Añadir una oferta al pipeline |
| `importar-ofertas.py` | Meter ofertas de un CSV en bloque |
| `ver-ofertas.py` | Qué hacer hoy |
| `ver-metricas.py` | El funnel y sus ratios |

Más `scripts/check-privacidad.py`, que va aparte porque no es del pipeline:
busca emails, teléfonos, DNIs, URLs de LinkedIn y rutas de disco antes de cada
commit y en cada push.

Detalles en [`4-ofertas/scripts/README.md`](4-ofertas/scripts/README.md).

## Qué no hace

Esto es la diferencia entre una herramienta y una tentación.

- **No envía candidaturas.** Ni por formulario, ni por API, ni por correo.
- **No hace login** en ningún portal. LinkedIn incluido.
- **No accede a tu correo, ni a tu calendario, ni a ninguna cuenta tuya.**
- **No accede a internet.** Ningún script abre una conexión.
- **No escribe fuera de tu disco.** Solo en los ficheros de este repo.

Lo de no enviar candidaturas no es una limitación técnica pendiente. Es una
decisión: automatizar el envío incumple los términos de casi todos los portales
de empleo, y la cuenta que se bloquea es la tuya. Ver [`SECURITY.md`](SECURITY.md).

## Privacidad

El `.gitignore` está montado para que sea difícil subir algo tuyo por error, y
`check-privacidad.py` busca datos personales antes de cada commit y en cada
push.

```console
$ python scripts/check-privacidad.py
Revisando 66 ficheros (todo el repositorio)
Palabras personales activas: 0

OK: no se ha encontrado ningun dato personal.
```

Los estados protegidos del pipeline (`Enviada`, `Seguimiento`, `Entrevista`,
`PruebaTecnica`, `Oferta`) no se pueden modificar por script. `escribir_pipeline()`
aborta la escritura y avisa de qué campo cambió, porque un pipeline que se
reescribe solo deja de ser un registro histórico.

Explicado en [`PRIVACY.md`](PRIVACY.md), que conviene leer una vez.

## Antes de compartir tu versión

```bash
python -m pytest 4-ofertas/tests/ -q
python scripts/check-privacidad.py --todo
```

Los dos en verde. El segundo importa más: este repo existe para no filtrar
nada.

## Trabajar con IA

Si tu IA lee `AGENTS.md`, ya tiene el contexto: qué es fuente de verdad, qué
no puede inventar, y que nada se envía.

Si no, hay un prompt listo en
[`docs/primeros-pasos-con-ia.md`](docs/primeros-pasos-con-ia.md). La versión
corta:

> Trabaja en un repo de búsqueda de empleo. `1-perfil-profesional/` es la fuente
> de verdad. No inventes experiencia, cifras ni tecnologías. Una pregunta cada
> vez. Nada de datos personales. Nada de enviar candidaturas ni automatizar
> portales.

## FAQ

**¿Puedo usarlo si no soy de España?**
Sí. Cambia los patrones de teléfono del escáner y los tipos de contrato de
`config.toml`. La estructura y los scripts no dependen de nada español.

**¿Por qué UNKNOWN no es lo mismo que remoto?**
Porque la oferta no lo dice. Confundir "no dice" con "es remoto" descarta
ofertas que sí encajaban, y por eso es un estado de verdad y no un valor por
defecto.

**¿Por qué los estados van sin acentos, como `PruebaTecnica`?**
Porque el pipeline es un CSV que se abre en Excel, en un editor de texto y a
veces en una terminal. `Prueba Técnica` y `PruebaTecnica` serían dos estados
distintos para el código. Los scripts aceptan las dos formas al leer.

**¿Puedo cambiar los pesos del encaje?**
Sí, en `[scoring]` de `config.toml`. El total es una media ponderada que se
normaliza por los pesos de las dimensiones que de verdad se pudieron evaluar,
así que una dimensión que tu config no permite calcular no te penaliza.

**¿Por qué el ejemplo no tiene datos reales?**
Porque si tuviera, se copiarían. Los ejemplos son ficticios a propósito y el
escáner falla si no.

**Mi empresa anterior aparece en un ejemplo. ¿Cómo lo quito?**
Añade la palabra a `palabras_prohibidas` en `config.toml` y vuelve a pasar el
escáner. Está pensado justo para eso.

## Requisitos

Python 3.11 o superior (usa `tomllib`). Nada más: los scripts son solo
librería estándar, y `pytest` solo hace falta para los tests. Funciona en
Windows, Linux, WSL y macOS.

## Licencia

MIT. Ver [`LICENSE`](LICENSE).
