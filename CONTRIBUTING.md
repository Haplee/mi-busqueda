# Como contribuir

Gracias por echar un vistazo. Cualquier corrección es bienvenida: un texto mal
explicado, un script que falla en tu sistema o una palabra que se entiende peor de
lo que parece.

## Lo unico obligatorio

**El repo no puede contener datos personales.** Ni los tuyos ni los de nadie. El CI
lo comprueba en cada push con `scripts/check-privacidad.py` y bloquea el merge si
encuentra un email, un teléfono, un DNI, una URL de LinkedIn o una ruta de tu
disco.

Lee `PRIVACY.md` antes de abrir el primer PR. Es corto.

## Antes de enviar

```bash
python -m pytest 4-ofertas/tests/ -q
python scripts/check-privacidad.py --todo
```

Los dos tienen que pasar. También hay una lista de verificación en la plantilla de
PR.

## Como hacer un cambio

1. **Una cosa por PR.** O un texto, o un script, o una carpeta. Mezclar hace la
   revisión más lenta.
2. **Explica el porqué.** El diff ya dice qué has cambiado; el cuerpo del PR debería
   decir por qué lo has cambiado.
3. **Los datos de ejemplo son inventados.** Si añades una oferta de muestra, que
   sea claramente ficticia: `Empresa Ficticia`, URLs de `example.com`, nada que
   parezca real.
4. **Los marcadores van entre corchetes.** `[TU_NOMBRE]`, `[TU_MINIMO_SALARIO]`.
   Así el escáner no los confunde con datos.

## Si añades un script

Míralo en `AGENTS.md`. Lo corto:

- rutas relativas, sin `C:\Users\...` ni `/home/...`
- sin red
- sin dependencias nuevas (la stdlib suele bastar)
- si escribe, pasa por `escribir_pipeline()`
- test propio en `4-ofertas/tests/`
- una fila en `4-ofertas/scripts/README.md`

## Si traduces el repo

Todo está en español y se va a mantener en español, al menos mientras el proyecto
no tenga traducción oficial. Si quieres añadir una, déjala en un `README.<idioma>.md`
en la raíz y avisa antes de tocar el resto: los scripts tienen mensajes de error que
también cuentan como documentación.

## Reportar un problema de seguridad

No abras un issue público. Usa el aviso privado de GitHub: **Security** → **Report
a vulnerability**. Ver `SECURITY.md`.

## Código de conducta

Sé claro y respetuoso. Discute la idea, no a la persona. Si algo no lo entiendes,
pregunta antes de suprimirlo.

## Código

MIT. Ver `LICENSE`.
