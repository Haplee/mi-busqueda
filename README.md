# mi-busqueda

Una plantilla para llevar la búsqueda de empleo como se lleva una búsqueda de
empleo: con un objetivo escrito, un perfil que se reuse, un pipeline de ofertas
y un seguimiento de lo que ya has enviado.

La diferencia con una carpeta llena de CV es que el CV se genera. Todo lo demás
sale de `1-perfil-profesional/`.

## Para quién es

Para quien busca empleo y ya tiene su historia escrita, pero la está
reorganizando cada semana en documentos con nombre tipo
`cv_final_v3_REAL.pdf`.

En concreto, para quien:

- quiere que el CV, el LinkedIn y la carta digan lo mismo
- pierde ofertas por no acordarse de hacer el seguimiento
- no sabe si está aplicando a demasiada o a ninguna
- prefiere el CV de una página al de tres, y no por pereza
- tiene veinte pestañas de ofertas abiertas y ninguna decisión tomada

No es para quien acaba de empezar de cero. Empieza por
`0-objetivo-y-estrategia/objetivo.md`, que está pensado para eso.

## Qué NO hace

Esto importa leerlo, porque es la diferencia entre una herramienta y una
tentación.

- **No envía candidaturas.** Ni por formulario, ni por API, ni por correo.
- **No hace login** en ningún portal. LinkedIn incluido.
- **No accede a tu correo, ni a tu calendario, ni a ninguna cuenta tuya.**
- **No accede a internet.** Ningún script abre una conexión.
- **No escribe fuera de tu disco.** Solo en los ficheros de este repo.
- **No aplica filtros automáticos a ofertas por ti.** La decisión es tuya.
- **No te dice qué puesto te conviene.** Te dice qué has comparado.
- **No contiene datos de nadie.** Ni los tuyos, ni los de tu ejemplo.

Lo de no enviar candidaturas no es una limitación técnica pendiente de
resolver. Es una decisión: automatizar el envío incumple los términos de casi
todos los portales de empleo, y la cuenta que se bloquea es la tuya. Ver
`SECURITY.md`.

## Instalación

```bash
git clone <tu-fork>
cd mi-busqueda
```

No hay dependencias que instalar para usar los scripts. Todo es Python estándar.

Para correr los tests:

```bash
python -m pip install pytest
```

Requiere Python 3.11 o superior (usa `tomllib`). Funciona en Windows, Linux, WSL
y macOS.

## Primer uso

### 1. Decide el objetivo

```bash
open 0-objetivo-y-estrategia/objetivo.md
```

Aquí es donde decides qué puestos buscas y cuáles descartas. Es la parte más
importante y la que más gente se salta.

### 2. Escribe el perfil

```bash
open 1-perfil-profesional/README.md
```

Rellena `experiencia.md`, `formacion.md`, `habilidades.md` y
`banco-de-logros.md`. Da igual que sea a medias. Da igual que tarde dos
tardes.

Esta carpeta es la fuente de verdad. Si algo no está aquí, no existe, aunque
recuerdes haberlo hecho.

### 3. Configura los filtros

```bash
cp 4-ofertas/config.example.toml 4-ofertas/config.toml
```

Modalidades, contratos, salario mínimo, palabras que excluyen una oferta. Todo
lo que el script debe descartar por ti.

`config.toml` está en `.gitignore`. Es tuyo.

### 4. Crea tu pipeline

```bash
cp 4-ofertas/pipeline.example.csv 4-ofertas/pipeline.csv
```

También ignorado por git.

### 5. Añade ofertas

```bash
python 4-ofertas/scripts/agregar-oferta.py \
    --empresa "Nombre S.L." --puesto "Tecnico de soporte" \
    --url "https://..." --estado Detectada
```

O de golpe, si ya tienes ofertas guardadas en otro sitio:

```bash
python 4-ofertas/scripts/importar-ofertas.py ofertas.csv --dry-run
```

### 6. Mira qué toca

```bash
python 4-ofertas/scripts/ver-ofertas.py
```

### 7. Revisa las cifras, de vez en cuando

```bash
python 4-ofertas/scripts/ver-metricas.py
```

## Estructura

```
mi-busqueda/
├── 0-objetivo-y-estrategia/   Qué buscas y qué descartas
├── 1-perfil-profesional/      Fuente de verdad. El CV sale de aquí
├── 2-documentos/              CV, carta, emails
├── 3-presencia-online/        LinkedIn, GitHub, portfolio
├── 4-ofertas/                 Pipeline, config y scripts
├── 5-postulaciones/           Una carpeta por candidatura. Ignorada por git
├── 6-entrevistas/
├── 7-networking/
├── 8-seguimiento/
├── 9-recursos/
├── docs/
├── examples/
└── scripts/                   Solo el escáner de privacidad
```

El número del principio no es decorativo: es el orden en el que se rellena.
Desde la 0 a la 9, en ese orden, y la 1 antes que la 2.

## Los scripts

Cuatro, todos locales y sin dependencias:

| Script | Para qué |
|--------|----------|
| `agregar-oferta.py` | Añadir una oferta al pipeline |
| `importar-ofertas.py` | Meter ofertas de un CSV en bloque |
| `ver-ofertas.py` | Qué hacer hoy |
| `ver-metricas.py` | El funnel y sus ratios |

Más el escáner de privacidad, que vive fuera porque no es del pipeline:
`scripts/check-privacidad.py`.

Detalles en [`4-ofertas/scripts/README.md`](4-ofertas/scripts/README.md).

## Privacidad

El `.gitignore` está montado para que sea difícil subir algo tuyo por error, y
`scripts/check-privacidad.py` busca emails, teléfonos, DNIs, URLs de LinkedIn y
rutas de disco antes de cada commit.

```bash
python scripts/check-privacidad.py
```

Está también como hook de git y como paso del CI. Explicado en
[`PRIVACY.md`](PRIVACY.md), que conviene leer una vez.

## Ejemplo

`examples/perfil-ficticio/` tiene el recorrido completo con datos inventados:
perfil, un par de ofertas y una postulación. Sirve para ver el resultado sin
mezclarlo con lo tuyo, y para saber qué se espera de cada fichero.

## Trabajar con IA

Si tienes una IA que lea `AGENTS.md` o `CLAUDE.md`, ya tiene el contexto.

Si no, hay un prompt listo en
[`docs/primeros-pasos-con-ia.md`](docs/primeros-pasos-con-ia.md). La versión
corta:

> Trabaja en un repo de búsqueda de empleo. `1-perfil-profesional/` es la fuente
> de verdad. No inventes experiencia, cifras ni tecnologías. Una pregunta cada
> vez. Nada de datos personales. Nada de enviar candidaturas ni automatizar
> portales.

## Antes de compartir tu versión

```bash
python -m pytest 4-ofertas/tests/ -q
python scripts/check-privacidad.py --todo
```

Los dos en verde. El segundo importa más: este repo existe para no filtrar
nada.

## FAQ

**¿Puedo usarlo si no soy de España?**
Sí, en cuanto cambies los patrones de teléfono en el escáner y los tipos de
contrato de `config.example.toml`. La estructura de carpetas y los scripts no
dependen de nada español.

**¿Los scripts van a fallar con ofertas de otro país?**
Las modalidades y los contratos de `config.example.toml` están pensados para
España. Añade los tuyos; el script compara por igualdad, no por rangos cerrados.

**¿Puedo cambiar el esquema del CSV?**
Puedes, pero `utilidades.py` tiene las columnas fijas. Si las cambias, cambia
`COLUMNAS` y actualiza `pipeline.example.csv` y los tests.

**¿Por qué UNKNOWN no es lo mismo que remoto?**
Porque la oferta no lo dice. Confundir "no dice" con "es remoto" descarta ofertas
que sí encajaban. Ver `4-ofertas/scripts/README.md`.

**¿Puedo meter datos reales en los ejemplos?**
No. Los ejemplos son ficticios a propósito, y el escáner falla si no.

**¿Puedo usarlo en una carpeta que no sea un repo git?**
Sí. Los scripts no dependen de git. Solo el escáner usa `git diff --cached` para
saber qué va a commitear, y si no encuentra git revisa todo.

**Mi empresa anterior aparece en un ejemplo. ¿Cómo lo quito?**
Añade la palabra a `palabras_prohibidas` en `config.toml` y vuelve a pasar el
escáner. Está pensado justo para eso.

## Licencia

MIT. Ver [`LICENSE`](LICENSE).
