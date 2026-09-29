## Que hay que tener en cuenta

Este repo tiene una regla que va por delante del estilo: **no puede contener
datos personales**. El CI lo comprueba en cada push, asi que si te falla la
privacidad, el commit no entra.

## Antes de abrir el PR

- [ ] `python -m pytest 4-ofertas/tests/ -q` pasa
- [ ] `python scripts/check-privacidad.py --todo` pasa
- [ ] `python -m compileall 4-ofertas/scripts scripts` no da errores
- [ ] He releido el diff buscando mi nombre, email, telefono o rutas de mi maquina
- [ ] Los datos de ejemplo son de ejemplo, no mios

## Si has tocado un script

- [ ] Usa rutas relativas (`Path(__file__).resolve()`), nunca absolutas
- [ ] No accede a la red
- [ ] Si escribe, pasa por `escribir_pipeline()` y documenta el backup
- [ ] Tiene test en `4-ofertas/tests/`
- [ ] Esta documentado en `4-ofertas/scripts/README.md`

## Si has tocado un documento

- [ ] Los huecos son marcadores `[TU_...]`, no datos inventados
- [ ] No hay experiencia, cifras ni tecnologias que no sean reales
- [ ] El documento sigue siendo generico: sirve para otra persona sin cambios

## Convenciones

- Español, con tuteo.
- `UNKNOWN` no es `REMOTO`. Cuando la oferta no lo dice, no lo inventes.
- Comentarios que explican por que, no que.
- Sin emojis.
- Si has anadido una seccion numerada, actualiza tambien el README de la raiz.

## Que hace el CI

1. `check-privacidad.py --todo` sobre el contenido del repo
2. `pytest 4-ofertas/tests/`
3. `compileall` de todos los scripts

Los tres tienen que pasar. El primero es el que mas importa.
