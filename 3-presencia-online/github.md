# GitHub — auditoría y plan

> Checklist, no ejecución automática. Nada aquí accede a tu cuenta.

**Usuario:** [TU_USUARIO_DE_GITHUB]
**Perfil:** [TU_URL]
**Última revisión:** [AAAA-MM-DD]

## Qué mira alguien que te está evaluando

En este orden, y con poco tiempo cada uno:

1. **El perfil** — bio, avatar, README. 10 segundos.
2. **Los repos fijados** — 6 huecos. 30 segundos.
3. **Un repo abierto al azar** — el README. 1 minuto.

Si pasas las tres, ya no estás en la bandeja de "a lo mejor". Si fallas la tercera,
da igual lo bien que estén las dos primeras.

## Perfil

- [ ] Bio: qué haces, en una línea, con un verbo
- [ ] Avatar reconocible
- [ ] Email de contacto visible (o al menos el dominio del portfolio)
- [ ] `README.md` en `TU_USUARIO/TU_USUARIO` (repo especial del perfil)
- [ ] Location y pronouns, opcional

**README del perfil** — estructura mínima:

```markdown
# Tu nombre

Qué haces. Con qué. Qué buscas.

## Contacto
- [Email]
- [LinkedIn]
- [Portfolio]

## Repos destacados
- [nombre](url) — una frase de qué es y qué tiene de interesante
```

La sección "Repos destacados" del README es un plus: muestra en la propia página del perfil
lo que fijaste en la pestaña de repos.

## Repos: qué merece la pena arreglar

No todos tus repos valen lo mismo. Criterio, de mayor a menor valor:

| Tipo | Por qué | Acción |
|------|---------|--------|
| Proyecto personal terminado | Demuestra que terminas cosas | Pinear y documento bien |
| Proyecto de formación | Demuestra que aplicas lo aprendido | Pinar si es bueno |
| Contributions a otros | Demuestra colaboración | Destacar en el perfil |
| Script o herramienta | Demuestra utilidad práctica | Pinar si está limpo |
| Hello world, forks, pruebas | No aporta nada | Archivar, no borrar |

**No borres repos por vergüenza: archívalos.** Un repositorio archivado sigue
existiendo y casi nadie te lo tiene en cuenta. Uno vacío y público tampoco, pero
ocupa lugar en tus fijados.

## Checklist por repositorio

- [ ] Descripción de una línea, con un verbo
- [ ] Topics (5-10): Technologies que se buscan con `topic:` en GitHub
- [ ] README con:
  - [ ] Qué hace, en dos frases
  - [ ] Captura o GIF (si es algo visual)
  - [ ] Stack
  - [ ] Instalación / uso
  - [ ] Licencia
- [ ] `LICENSE` si es tuyo
- [ ] Live demo o enlace a la versión desplegada, si aplica

El README es lo que más se subestima. Casi nadie lo mira, y es lo que más convierte.

## Configuración

- [ ] Autenticación en dos factores activada
- [ ] Email de recuperación configurado
- [ ] Correos públicos de confirmación: desactivados
- [ ] `github.com/settings/tokens` revisado: tokens antiguos eliminados

## Repos y privacidad

Un aviso que aplica a todos los repos, no solo a GitHub:

**Este repo es una plantilla pública. Tus proyectos personales van en tu cuenta, no aquí.**

Ver `PRIVACY.md` para las reglas completas.

Si trabajas en algo con datos de clientes o NDA, no lo publiques: ni público, ni
privado si contiene secretos. La opción segura es un repositorio local sin remoto.

## Checklist de repos

| Repositorio | Descripción | Topics | README | License | Fijado |
|-------------|------------|--------|--------|---------|--------|
| [REPO_1] | Sí/No | Sí/No | Sí/No | Sí/No | Sí/No |
| [REPO_2] | Sí/No | Sí/No | Sí/No | Sí/No | Sí/No |
| [REPO_3] | Sí/No | Sí/No | Sí/No | Sí/No | Sí/No |

Objetivo: 6 fijados, todos con README. Mejor 4 buenos que 6 con uno sin documentar.
