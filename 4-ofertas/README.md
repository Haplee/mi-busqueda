# 4 — Ofertas

Todo lo relacionado con encontrar ofertas y gestionarlas. Es la carpeta con más scripts,
porque es la que más trabajo manual ahorra.

## Contenido

| Archivo / carpeta | Qué es |
|-------------------|--------|
| `pipeline.example.csv` | **La única versión de pipeline que hay en git.** Cabecera + 2 filas ficticias |
| `config.example.toml` | Tu configuración. Copia a `config.toml`, que está ignorado por git |
| `plantilla-oferta.md` | Ficha para guardar cada oferta que te interesa |
| `empresas-objetivo.md` | Lista de empresas a las que quieres entrar de verdad |
| `alertas.md` | Configuración de alertas de búsqueda |
| `scripts/` | Scripts reutilizables, con tests |
| `tests/` | Tests de los scripts (`pytest`) |

## Tu pipeline real

El repo **no** trae `pipeline.csv`. Se crea la primera vez:

```bash
cp 4-ofertas/pipeline.example.csv 4-ofertas/pipeline.csv
```

Está en `.gitignore`, y con razón: contiene las ofertas concretas a las que te{cases
o envías, que es información sobre ti, no sobre la plantilla.

## Los estados del pipeline

El orden importa: una candidatura avanza hacia abajo.

```
Detectada → Revisada → Interesante → Ajustada → Enviada
                                                   ↓
                            Sin respuesta ← Entrevista → PruebaTecnica → Oferta
                                                   ↓
                                    Sin respuesta
```

| Estado | Significa |
|--------|-----------|
| `Detectada` | Vista, sin decidir |
| `Revisada` | Leída, sin decidir si aplica |
| `Interesante` | Encaja, pendiente de preparar |
| `Ajustada` | Carpeta de postulación preparada |
| `Enviada` | Candidatura enviada |
| `SinRespuesta` | Sin respuesta tras el seguimiento |
| `Seguimiento` | Seguimiento enviado, esperando |
| `Entrevista` | Hay entrevista |
| `PruebaTecnica` | Prueba técnica en curso |
| `Oferta` | Oferta formal recibida |
| `Rechazada` | Descartada por la empresa |
| `Descartada` | Descartada por ti |
| `EJEMPLO` | Fila de prueba o demo. **No cuenta en las métricas** |

Sin acentos en los estados, a propósito: el pipeline es un CSV que se abre en
Excel, en un editor de texto y a veces en una terminal, y `Prueba Técnica` frente
a `PruebaTecnica` son dos estados distintos para el código. Los scripts aceptan
las dos formas al leer y siempre escriben la segunda.

## Los cinco estados protegidos

```
Enviada   Seguimiento   Entrevista   PruebaTecnica   Oferta
```

Ningún script puede modificar una fila en estos estados. Ni la modalidad, ni el
estado, ni las notas, ni la fecha de envío, ni el salario.

La comprobación está en `escribir_pipeline()`, que es el único punto del repo que
escribe: compara el estado anterior y el nuevo y **aborta la escritura** si una
fila protegida cambió. El backup se crea después de esa comprobación, así que un
intento fallido ni siquiera genera un fichero nuevo.

Los tests que lo garantizan están en `tests/test_estados_protegidos.py`:
no se puede cambiar el estado, ni ningún otro campo, ni eliminar la fila, ni
avanzarla a otro estado protegido.

La razón es simple: si un script puede reescribir una fila que ya enviaste, se
pierde el histórico y tus métricas dejan de significar nada. Y si tienes que
cambiar una candidatura enviada, se cambia a mano en el CSV.

## Estructura de una fila

```csv
ID,Fecha,Empresa,Puesto,Ubicacion,Modalidad,Contrato,Salario,Fuente,URL,Estado,Contacto,ProximaAccion,FechaSeguimiento,Encaje,Notas
```

| Campo | Notas |
|-------|-------|
| `ID` | Fecha + empresa + puesto, sin espacios ni acentos. Único |
| `Fecha` | Cuándo la viste, no cuándo la enviaste |
| `Estado` | Solo valores de la tabla de arriba |
| `Encaje` | `1-10`, o `EJEMPLO` en las filas de ejemplo |
| `FechaSeguimiento` | Cuándo toca seguir. Vacío si no aplica |
| `Notas` | Sin comas sin escapar. Usa `;` en vez de `,` |

## Scripts

```bash
python 4-ofertas/scripts/ver-ofertas.py        # qué hacer hoy
python 4-ofertas/scripts/agregar-oferta.py     # añade una oferta
python 4-ofertas/scripts/importar-ofertas.py   # mete ofertas de un CSV en bloque
python 4-ofertas/scripts/ver-metricas.py       # métricas y ratios del funnel
```

Detalle en `scripts/README.md`.

## Lo que los scripts NO hacen

- No envían candidaturas
- No hacen login en ningún portal
- No acceden a LinkedIn ni a tu correo
- No acceden a internet
- No escriben fuera de tu máquina

Ver `PRIVACY.md` y `SECURITY.md`.
