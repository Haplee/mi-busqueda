# Alertas de búsqueda

> Configura alertas para que las ofertas lleguen a ti. El objetivo es no tener que buscar
> cada día: solo revisar.

## Principio

Una alerta bien configurada es un filtro que trabaja por ti. Una mal configurada es ruido
que te hace dejar de mirar el correo.

**Criterio:** si en dos semanas recibes más de 15 alertas y solo te interesan 2, el
problema es el filtro de la alerta, no tu falta de tiempo.

## Fuentes y dónde buscar

| Fuente | Qué encuentra | Nota |
|--------|---------------|------|
| [FUENTE_1] | [QUÉ_TIPOS] | [CÓMO_FUNCIONA] |
| [FUENTE_2] | | |
| [FUENTE_3] | | |

> Este repo **no** automatiza la búsqueda ni accede a cuentas. Lee `PRIVACY.md`.
> Estas alertas son las que configures tú, a mano, en cada portal.

## Alertas activas

| # | Portal | Término de búsqueda | Filtros | Frecuencia | Última revisión |
|---|--------|--------------------|---------|------------|-----------------|
| 1 | [PORTAL] | [TUS_KEYWORDS] | [MODALIDAD] | Diaria | [AAAA-MM-DD] |
| 2 | [PORTAL] | [TUS_KEYWORDS] | | Diaria | |
| 3 | [PORTAL] | | | Semanal | |

## Cómo elegir los términos de búsqueda

Usa **sinónimos**, no un único término. El mismo puesto se llama de cinco formas:

```
[TU_PUESTO]
[SINONIMO_1]
[SINONIMO_2]
[EL_TÉRMINO_EN_EL_IDIOMA_DEL_PAIS_OBJETIVO]
```

Los mismos valores van en `4-ofertas/config.toml`, sección `[busqueda] keywords`. Así el
script y las alertas buscan lo mismo.

## Qué poner en cada alerta

| Campo | Recomendación | Por qué |
|-------|---------------|---------|
| Modalidad | [TU_MODALIDAD] | Filtra ruido desde el origen |
| Contrato | Tus aceptados | Evita revisar lo que no vas a candidatar |
| Antigüedad de la publicación | Última semana | Las ofertas buenas se llenan rápido |
| Frecuencia | Diaria | Semanal te hace perder las buenas |
| Notificación | Email, no push | El push se ignora sin leer |

## Qué alertas NO configurar

| No hagas esto | Por qué |
|---------------|---------|
| Alertas con 5 sinónimos sin filtrar | Llega todo, no miras nada |
| Alertas de "cualquier puesto" | Ruido puro |
| Alertas de empresas concretas que no has evaluado | No sabes todavía si te sirven |
| Alertas sin fecha de última revisión | Se acumulan y caducan sin que lo sepas |

## Revisión mensual

Cada 30 días:

- [ ] ¿Cuántas alertas llegaron? ¿Cuántas me sirvieron?
- [ ] ¿Sigo teniendo la alerta, o ya la cancelé mentalmente?
- [ ] ¿Algún término está trayendo cero resultados?
- [ ] ¿Apareció alguna fuente nueva que merezca entrar en la tabla?

> Una alerta que lleva dos meses sin servirte de nada es una alerta que debes borrar.

## Nota sobre automatización

Este repo no envía alertas por ti ni se conecta a portales. Su parte automatizada se
limita a **leer ofertas públicas** y a calcular métricas locales. Ver `PRIVACY.md`.
