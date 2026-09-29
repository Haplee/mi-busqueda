# Scripts

Todos los scripts son locales, de solo lectura o con escritura controlada, y
funcionan en Windows, Linux y WSL sin cambiar nada.

## Instalación

Ninguna dependencia externa, salvo `pytest` para los tests.

```bash
python -m pip install pytest
```

Los scripts usan `tomllib`, que viene con Python 3.11 o superior.

## Configuración

Los filtros **no están en el código**: salen de `4-ofertas/config.toml`.

```bash
cp 4-ofertas/config.example.toml 4-ofertas/config.toml
```

Si el script se ejecuta sin `config.toml`, funciona con valores vacíos: avisa por
pantalla y no filtra nada. Prefiere no decidir a decidir por ti.

## Los scripts

### `ver-ofertas.py` — qué hacer hoy

```bash
python 4-ofertas/scripts/ver-ofertas.py
```

| | |
|---|---|
| **Qué hace** | Lee el pipeline y agrupa las ofertas por lo que necesitan de ti: seguimientos atrasados, seguimientos de esta semana, enviadas sin respuesta hace más de 3 semanas, ofertas interesantes sin preparar |
| **Qué modifica** | Nada |
| **Lee** | `4-ofertas/pipeline.csv`, `4-ofertas/config.toml`, `1-perfil-profesional/habilidades.md` |
| **Argumentos** | `--pipeline RUTA` |

Muestra el encaje por dimensión, no solo el total. Un `7/10` no dice si el problema
es el idioma, la ubicación o el contrato.

### `agregar-oferta.py` — añadir una oferta

```bash
python 4-ofertas/scripts/agregar-oferta.py \
    --empresa "Nombre S.L." \
    --puesto "Tecnico de soporte" \
    --url "https://..." \
    --modalidad "Remoto" \
    --estado Detectada
```

| | |
|---|---|
| **Qué hace** | Añade una fila al final del pipeline |
| **Qué modifica** | `4-ofertas/pipeline.csv`. Crea `pipeline.csv.bak` antes |
| **Argumentos** | `--empresa` (obligatorio), `--puesto` (obligatorio), `--url`, `--ubicacion`, `--modalidad`, `--contrato`, `--salario`, `--fuente`, `--contacto`, `--estado`, `--encaje`, `--seguimiento-dias`, `--notas`, `--pipeline` |

**Nunca sobrescribe.** Si la URL ya existe, avisa y no hace nada. Esto evita
tener tres filas de la misma oferta con estados distintos, que es como se rompe un
pipeline.

Lo que no se puede determinar queda como `UNKNOWN`. No infiere modalidad ni contrato
a partir del título.

### `ver-metricas.py` — el funnel

```bash
python 4-ofertas/scripts/ver-metricas.py
python 4-ofertas/scripts/ver-metricas.py --desde 2026-01-01
```

| | |
|---|---|
| **Qué hace** | Calcula volumen por estado, el embudo y sus ratios, y desgloses por portal, modalidad y encaje |
| **Qué modifica** | Nada |
| **Argumentos** | `--pipeline RUTA`, `--desde AAAA-MM-DD` |

Las filas con `Estado = EJEMPLO` se excluyen de **todas** las cifras. Una prueba no
es una candidatura, y contarla falsea el diagnóstico.

Avisa cuando el volumen es bajo: por debajo de 20 candidaturas, los ratios no
significan nada todavía.

### `importar-ofertas.py` — meter ofertas en bloque

```bash
python 4-ofertas/scripts/importar-ofertas.py ofertas.csv --dry-run
python 4-ofertas/scripts/importar-ofertas.py ofertas.csv
```

| | |
|---|---|
| **Qué hace** | Lee un CSV de ofertas y añade las que no están en el pipeline |
| **Qué modifica** | `4-ofertas/pipeline.csv`, con backup previo |
| **Argumentos** | `--pipeline RUTA`, `--columnas destino:entrada`, `--estado`, `--dry-run` |

Empareja columnas por nombre automáticamente. Si tu CSV usa otros nombres:

```bash
python 4-ofertas/scripts/importar-ofertas.py ofertas.csv \
    --columnas "Puesto:title,Empresa:company,URL:link"
```

**Usa `--dry-run` antes de la primera vez.** Te dice cuántas añadiría, cuántas son
duplicadas y cuántas van a quedar fuera por estar incompletas.

## Qué NO hace ningún script

- **No envía candidaturas.** Ni por formulario, ni por API, ni por email.
- **No hace login** en ningún portal.
- **No accede a LinkedIn**, ni a tu correo, ni a ninguna cuenta tuya.
- **No escribe fuera de tu máquina.**
- **No modifica filas en estado protegido** (`Enviada`, `Seguimiento`,
  `Entrevista`, `PruebaTecnica`, `Oferta`).

Sobre por qué: `PRIVACY.md` y el README de la raíz. Automatizar el envío de
candidaturas incumple los términos de casi todos los portales de empleo y es la vía
más rápida a que te bloqueen la cuenta.

## Script que sí escribe

Solo uno: `agregar-oferta.py`, y a través de `importar-ofertas.py`. Los dos pasan
por `escribir_pipeline()`, que es el único sitio del repo que escribe en
`pipeline.csv` y que siempre crea el backup antes.

## Tests

```bash
python -m pytest 4-ofertas/tests/ -v
```

Qué cubren, y por qué existe cada cosa:

| Fichero | Qué protege |
|---------|-------------|
| `test_parsers.py` | Que `UNKNOWN` no se convierta nunca en `REMOTO`, y que el parser no consulte la config |
| `test_estados_protegidos.py` | Que las filas en estado protegido no se toquen, y que toda escritura cree backup |
| `test_pipeline.py` | Duplicados, backup rotativo, rutas portables, y que el único CSV en git sea el de ejemplo |

Los tests usan datos ficticios y CSV temporales. No tocan tu `pipeline.csv`.

## Añadir un script nuevo

1. Rutas relativas: `Path(__file__).resolve().parents[N]`. Nunca `C:\Users\...`.
2. Sin preferencias personales en el código. Si es una decisión tuya, va en `config.toml`.
3. Si escribe, pasa por `escribir_pipeline()`.
4. Si lee, no escribe nunca.
5. Añade un test a `4-ofertas/tests/`.
6. Documéntalo aquí, en una tabla como las de arriba.
