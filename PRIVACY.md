# Privacidad

Este repositorio está pensado para usarse en público. Eso obliga a una regla: **el
repo nunca contiene datos tuyos**.

No es una recomendación. La historia de este repositorio empieza con una carpeta
de trabajo con tu nombre, tu teléfono, tus candidaturas reales y un montón de
correos, y con la decisión de no subir nada de eso. Todo lo que hay aquí son
plantillas, un perfil ficticio y scripts que no tocan tus cuentas.

## Qué hay en `.gitignore` y por qué

| Patrón | Qué protege |
|--------|-------------|
| `config.toml` | Tus filtros, modalidades y palabras prohibidas |
| `4-ofertas/pipeline.csv` | Tus candidaturas reales. Solo se versiona `pipeline.example.csv` |
| `4-ofertas/pipeline.csv.bak*` | El backup del pipeline |
| `5-postulaciones/*` | Cartas, CVs y notas de ofertas reales. Solo se versiona `EJEMPLO_*` |
| `*.pdf`, `*.docx`, `*.xlsx` | Documentos que llevan tu nombre dentro |
| `datos-personales/`, `mis-datos/`, `personal/` | Tus notas privadas |
| `.env*` | Claves de API, si algún día conectas algo |
| `_archivo/`, `_retirados*/` | Lo que moviste de sitio y sigue ahí |
| `*.log`, `__pycache__/`, `.venv/` | Ruido |

El orden importa: se ignoran primero y se desbloquean después. Por eso
`4-ofertas/pipeline.example.csv` sí se versiona aunque el patrón `pipeline.csv`
esté en la lista.

## El script: `scripts/check-privacidad.py`

```bash
# Lo que estás a punto de commitear
python scripts/check-privacidad.py

# Todo el repo, por si acaso
python scripts/check-privacidad.py --todo
```

Detecta:

- emails
- teléfonos españoles (`6xx`, `7xx`, `8xx`, `9xx` con prefijo opcional)
- DNI y NIE
- URLs de `linkedin.com/in/`
- rutas `C:\Users\...` y `/home/...`
- las palabras que tú hayas puesto en `palabras_prohibidas`

Los dominios reservados por la RFC 2606 (`example.com`, `example.org`,
`example.net`) y cualquier dominio con `ejemplo` en él se consideran ficticios y
no se marcan. Es la diferencia entre un email de plantilla y uno de verdad.

Los ficheros de datos reales (`pipeline.csv`, `datos-personales/`, backups) están
excluidos del escaneo: no están en git, así que no pueden filtrarse por git, y
contenerían falsos positivos legítimos.

### Salida

```
Revisando 3 ficheros (ficheros preparados para commit)
Palabras personales activas: 4

OK: no se ha encontrado ningun dato personal.
```

O:

```
2 hallazgo(s):

  1-perfil-profesional/README.md:14  [email]  nombre.apellido@ejemplo-real.com

Como resolverlo:
  - Usa marcadores: [TU_NOMBRE], [TU_EMAIL], [TU_USUESTO]
  - Revisa PRIVACY.md
  - Si es un dato que debe estar, anadelo a EXCLUIDOS en este script
```

Sale con código `1` si encuentra algo, así que sirve como hook.

## Marcadores, no datos

En la plantilla, los huecos son texto entre corchetes:

```markdown
- **Nombre**: [TU_NOMBRE]
- **Email**: [TU_EMAIL]
- **LinkedIn**: [TU_LINKEDIN]
- **Salario mínimo**: [TU_MINIMO_SALARIO]
```

El escáner no los marca: `[TU_EMAIL]` no es una dirección, es una instrucción.
Y el repo se puede leer entero sin saber nada de ti.

## Palabras prohibidas

Si tienes palabras que te identifican (el nombre de una empresa anterior, el
nombre de tu ciudad, un alias), añádelas a `config.toml`:

```toml
palabras_prohibidas = [
  "tu-empresa-anterior",
  "tu-alias",
]
```

El escáner las lee de ahí. Mientras uses solo `config.example.toml`, están
desactivadas: los valores del ejemplo son ficticios a propósito.

## Git hooks

Hay dos formas de activarlo, y puedes usar las dos.

**Automático**, añade esto a `.git/hooks/pre-commit`:

```bash
#!/bin/sh
python scripts/check-privacidad.py || {
    echo ""
    echo "Commit cancelado: hay datos personales en lo preparado."
    echo "Revisa PRIVACY.md"
    exit 1
}
```

**Manual**, una sola vez:

```bash
git config core.hooksPath .githooks
```

## Lo que este repo nunca hace

- **No envía candidaturas.** Ni formularios, ni API, ni correo.
- **No hace login** en ningún portal, incluido LinkedIn.
- **No accede a ninguna cuenta tuya.** Ni correo, ni calendario, ni redes.
- **No escribe fuera de tu máquina.** No hay red en ningún script.
- **No toca el navegador ni el sistema.** Los scripts leen y escriben ficheros.

Los motivos están en `SECURITY.md`, pero el resumen es que automatizar el envío
incumple los términos de casi todos los portales de empleo, y la cuenta que se
bloquea es la tuya.

## Si ya has subido algo

Si esto alguna vez se convierte en un repo público y te das cuenta tarde:

```bash
# 1. Añadirlo a .gitignore
# 2. Sacarlo del historial. Reescribe el historial, y con el.
# 1. Sacarlo del índice. Esto solo lo quita a partir de ahora.
git rm --cached datos-personales/mis-notas.md
git commit -m "Elimina datos personales"

# Si ya estaba publicado, reescribe el historial:
git filter-repo --path datos-personales/ --invert-paths
```

Reescribir el historial no borra nada de una copia ya descargada. Si el dato era
un email o un teléfono, da por hecho que está comprometido y cámbialo.
