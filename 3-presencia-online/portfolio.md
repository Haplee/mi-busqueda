# Portfolio — auditoría y plan

> Un portfolio sirve para una cosa: enseñar una cosa concreta que un CV no puede enseñar.
> Si no tienes esa cosa, un portfolio vacío no te resta, pero tampoco suma nada.

**URL:** [TU_URL]
**Repositorio:** [TU_REPO]
**Última revisión:** [AAAA-MM-DD]

## La pregunta que decide si lo haces

> ¿Tienes **un** proyecto o **una** contribución que alguien pueda mirar en dos
> minutos y entender por qué te contratan?

- **Sí** → el portfolio vale la pena, y solo necesita de 3 a 5 piezas.
- **No** → el portfolio no es tu prioridad ahora. Los repos en GitHub ya cumplen ese papel.

Esta es una decisión honesta. Un portfolio mediocre resta más de lo que suma.

## Estructura mínima que funciona

```
/            → Quién eres, qué haces, contacto. 30 segundos.
/proyectos/  → Un proyecto por página, con: problema, qué hiciste, resultado, demo
/cv          → El CV en PDF
```

**Solo eso.** Si hay que explicar la navegación, es demasiado complicado.

## Qué tiene que tener cada proyecto

Es lo que más se olvida y lo que más diferencia:

| Sección | Qué va aquí | Por qué importa |
|---------|-------------|-----------------|
| **Problema** | Qué problema resolvía y a quién le dolía | Sin esto, es un ejercicio técnico |
| **Tu rol** | Qué parte es tuya | Distingue un proyecto de un trabajo de equipo |
| **Cómo** | Decisión técnica principal y por qué | Demuestra criterio, que es lo que se busca |
| **Resultado** | Qué pasó después, con cifras si las hay | Sin esto no es un logro, es una tarea |
| **Qué aprendiste** | Un límite, un error, algo que rehacerías | El momento que genera confianza |

La sección "qué aprendiste" es la que casi nadie pone y la que más humaniza. Un proyecto
con un error explained y una decisión argumentada convence más que uno impecable sin
explicación.

## Lo que NO va en un portfolio

| No pongas | Por qué |
|-----------|---------|
| Un "acerca de" de tres párrafos sobre tu vida | Nadie lo lee |
| Todos tus proyectos | Cuatro buenos > veinte sin contexto |
| Capturas sin explicación | ¿Y? |
| Tu CV entero en HTML | Si lo quieres en PDF, no es un portfolio |
| Contacto solo con un formulario sin email visible | Fricción innecesaria |

## Interacción

Si metes alguna animación, que tenga propósito: mostrar algo que no se entiende estático, o
dar sensación de escala. Si es solo decoración, resta: molesta, ralentiza y no dice nada del
trabajo.

**Prueba de realidad:** ¿se ve bien en el móvil? La mayoría de las visitas llegan desde
en un teléfono, y la mayoría de portfolio con Three.js y mapas no lo están.

## Idiomas

Si te presentas en dos idiomas, rutas separadas (`/es/`, `/en/`) con selector visible. No
un portfolio "bilingüe" con ambas mezcladas: se lee como si no lo hubieras terminado en
ninguno.

## Checklist

- [ ] Se entiende qué haces en los primeros 5 segundos, sin hacer scroll
- [ ] Hay un enlace visible a contacto
- [ ] Al menos un proyecto con problema, rol, decisión y resultado
- [ ] Todos los enlaces externos funcionan
- [ ] Se ve bien en móvil (probado, no supuesto)
- [ ] Carga rápido en 4G
- [ ] No hay marcadores `[CAMPO]` sin sustituir
- [ ] Ningún dato personal que no quieras hacer público (ver `PRIVACY.md`)

## Antes de publicarlo

- [ ] `grep -ri "gmail\|teléfono\|C:\\\\Users" .` no devuelve nada inesperado
- [ ] `python scripts/check-privacidad.py` pasa
- [ ] Revisión de datos en las capturas de pantalla (pueden contener nombres de clientes)
