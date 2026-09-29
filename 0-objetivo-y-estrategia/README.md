# 0 — Objetivo y estrategia

La carpeta más importante del repo, y la que más gente deja sin rellenar. Sin esto, los
scripts no filtran nada útil y el pipeline se llena de ofertas que nunca ibas a candidat.

## Orden de trabajo

1. **`guia-de-filtros.md`** — léela primero. Explica por qué los filtros demasiado
   restrictivos son la causa nº1 de búsquedas con cero resultados.
2. **`objetivo.md`** — tus puestos, modalidades, contratos y salario. Estos valores son
   los que luego copiarás a `4-ofertas/config.toml`.
3. **`puestos-objetivo.md`** — qué roles persigues y cuáles descartas. Es más largo a
   propósito: obliga a pensar en requisitos no negociables.
4. **`propuesta-de-valor.md`** — tus tres palancas y sus pruebas. Rellenar esto suele
   revelar que todavía no tienes suficientes logros, y eso es información útil.

## Traducir a config

Cuando termines `objetivo.md`, copia los valores a `4-ofertas/config.toml`:

| En `objetivo.md` | En `config.toml` |
|------------------|------------------|
| Puesto principal y alternativos | `[busqueda] keywords` |
| Puestos que no quieres | `[busqueda] exclude_keywords` |
| Modalidad | `[preferencias] modalidades` |
| Tipo de contrato | `[preferencias] contratos` |
| Salario mínimo | `[preferencias] salario_minimo` |

## Archivos

| Archivo | Para qué sirve |
|---------|----------------|
| `objetivo.md` | Definición del puesto y de las condiciones aceptadas |
| `guia-de-filtros.md` | Cómo decidir filtros sin quedarte sin ofertas |
| `puestos-objetivo.md` | Qué roles persigues, cuáles descartas y por qué |
| `propuesta-de-valor.md` | Tus tres palancas, con pruebas reales detrás |

## Nota sobre datos reales

Este repo es una plantilla: aquí no hay ningún dato real. Tus decisiones van en tu copia
local. Si clonaste la plantilla y la vas a subir a GitHub, lee `PRIVACY.md` antes del
primer `git commit`.
