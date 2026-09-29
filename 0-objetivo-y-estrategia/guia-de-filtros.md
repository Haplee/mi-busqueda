# Guía de filtros: cómo decidirlos sin quedarte sin ofertas

Este archivo existe por una razón concreta: la mayoría de búsquedas de empleo se rompen
no por falta de ofertas, sino por **filtros demasiado restrictivos escritos en 5 minutos**.

## El problema

Una búsqueda con estos siete filtros:

```
presencial + indefinido + jornada completa + >30.000€
+ [CIUDAD] + inglés B2 + 3 años de experiencia
```

devuelve cero resultados casi siempre. No porque no haya trabajo, sino porque esos siete
requisitos **nunca coinciden a la vez**. Y como no ves nada, concluyes que el mercado está seco.

## Los tres errores más comunes

### 1. Usar "Y" cuando el mercado usa "O"

Enumera los tipos de contrato que quieres. ¿De verdad necesitas `Indefinido`?

En muchas búsquedas, `Temporal` e `Indefinido` no son dos oportunidades distintas: son
la misma oferta en dos fases, y muchas empresas contratan primero temporal con intención de
indefinido. Excluir temporal por defecto reduce tu volumen a la mitad.

**Regla práctica:** excluye un tipo de contrato solo si has confirmado que la oferta es
temporal *y sin posibilidad de conversión*. Si no lo has confirmado, déjalo pasar.

### 2. Poner el filtro de modalidad como puerta, no como ranking

Si escribes "solo remoto" en el buscador **y además** en tu `config.toml`, estás aplicando
el filtro dos veces. Y si además lo usas como puerta de entrada, dejas de ver las mejores
oportunidades presenciales de tu ciudad.

**Regla práctica:** el filtro de modalidad decide, pero revísalo cada 4 semanas con la
métrica de respuestas. Si una modalidad que habías descartado convierte mejor, reactívala.

### 3. Confundir "obligatorio" con "deseable"

Solo hay unos pocos requisitos que son de verdad bloqueantes:

- Permiso de trabajo válido
- Titulación exigida por la empresa **cuando es regulatoria**, no cuando es preferencia
- Idioma con nivel exigido por escrito en la oferta y que determines si puedes trabajar

Todo lo demás —años de experiencia, stack concreto, título universitario— es casi siempre
**deseable**. Trátalo como criterio de puntuación, no como filtro de eliminación.

## Cómo se traducen tus preferencias a config

Todo lo que decidas aquí vive en `4-ofertas/config.toml`. El código no tiene preferencias
hardcodeadas: si algo está en el script, es un bug.

```toml
[busqueda]
keywords = ["[TU_PUESTO]", "[SINONIMO]", "[OTRO_SINONIMO]"]
exclude_keywords = ["[LO QUE NO TE INTERESA]"]

[preferencias]
modalidades = ["[MODALIDAD]"]
contratos = ["[TIPO_DE_CONTRATO]"]
salario_minimo = 0
```

## Cómo revisar tus filtros (cada 4 semanas)

Míralo en la tabla que genera `4-ofertas/scripts/ver-metricas.py`.

| Métrica | Qué significa | Acción si va mal |
|---------|---------------|------------------|
| 0 ofertas detectadas en 7 días | Filtros demasiado restrictivos | Amplía modalidades primero, luego contratos. Nunca por salario primero |
| Muchas detectadas, 0 enviadas | Los filtros están bien, el criterio de encaje está mal calibrado | Revisa `fit_score`, no los filtros |
| Muchas enviadas, 0 respuestas | El problema no son los filtros, son el CV o la carta | Ver `8-seguimiento/metricas.md` |
| Respuestas pero 0 entrevistas | El perfil no coincide con lo que se anuncia | Ajusta `puestos-objetivo.md` |

**No diagnostiques con una sola semana de datos.** Da al menos 4 semanas o 20 candidaturas
antes de cambiar la estrategia. Con muestras pequeñas todo parece una tendencia.

## Dos objetivos distintos que conviene no mezclar

Sueles tener el objetivo profesional definido en el CV, y el objetivo *de búsqueda*
definido de otra manera distinta. Esto es normal y está bien: son cosas diferentes.

- El **CV** va dirigido a un puesto concreto.
- La **búsqueda** va dirigida a un conjunto de puestos.

Es perfectamente válido que busques tres puestos distintos y que solo el CV esté optimizado
para uno de ellos. Lo que no funciona es no saber cuál de los tres es cuál.

Si en tu caso son dos líneas muy separadas (por ejemplo, soporte técnico y desarrollo web),
considera mantener **dos CV maestros** en `2-documentos/CV/` y elegir cuál adaptar en cada
candidatura. Mezclarlos en un solo CV "híbrido" suele hacer que ninguno de los dos casos
convenza.

## Traducción a otros idiomas

La estructura está pensada para funcionar también en inglés. Para preparar una versión
en inglés:

1. Copia `0-objetivo-y-estrategia/` a `0-objetivo-y-estrategia.en/`.
2. Traduce el **contenido** (objetivo, propuesta de valor), no los marcadores `[CAMPO]`.
3. Deja los nombres de archivo en español para no romper los scripts.
4. Los scripts no dependen del idioma: filtran sobre `keywords` de tu `config.toml`.
