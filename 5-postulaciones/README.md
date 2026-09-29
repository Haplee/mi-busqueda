# 5. Postulaciones

Una carpeta por oferta. Dentro, lo que enviaste y lo que recibiste.

## Estructura

```
5-postulaciones/
├── EJEMPLO_Empresa_Ficticia/
│   ├── README.md
│   ├── oferta.md
│   ├── carta.md
│   ├── cv-ajustado.md
│   ├── notas.md
│   ├── email-enviado.md
│   └── respuestas/
└── 2026-01-15_empresa-puesto/
    └── ...
```

El nombre de la carpeta es el ID del pipeline. Así se relaciona sin tener que
recordarlo.

## Qué va en cada fichero

| Fichero | Qué es |
|---------|--------|
| `oferta.md` | Copia de la oferta, con fecha. Apunta al original |
| `carta.md` | La carta que enviaste, tal cual |
| `cv-ajustado.md` | El CV de esa candidatura, con los cambios marcados |
| `notas.md` | Por qué la elegiste, qué te preocupaba, qué aprendiste |
| `email-enviado.md` | El email con su fecha y hora |
| `respuestas/` | Lo que te contestaron, con la fecha |

Guardar lo que enviaste tiene un motivo concreto: dentro de tres meses no te
acordarás de qué versión del CV mandaste a quién, y en una entrevista eso es una
pregunta incómoda.

## Privacidad

**Esta carpeta no se sube a git.** Solo `EJEMPLO_*` se versiona, y está en
`.gitignore` con una excepción explícita.

Si necesitas tener una postulación real en otra parte del disco, no la pongas aquí.
Esta carpeta es para lo que has enviado, y eso lleva tu nombre.

## Nombres de ficheros

Sin acentos ni espacios. La razón es práctica: algunos programas y algunas
terminales los rompen, y dentro de seis meses no vas a recordar por qué pusiste
aquí un `ñ` y allí no.

```
empresa-con-guion.md      si
empresa_con_guion.md      no
empresa con guion.md      no
```

## Qué hacer al recibir una respuesta

1. Copia el email a `respuestas/` con la fecha en el nombre.
2. Pasa la fila del pipeline al estado correspondiente: `Seguimiento`, `Entrevista`,
   `PruebaTecnica`, `Oferta` o `Rechazada`.
3. Escribe en `notas.md` qué pasó. Cuando llegue la hora de comparar opciones, esa
   es la información que vas a necesitar.
4. Si hubo llamada, anota las preguntas que te hicieron. Para la siguiente
   entrevista es oro.
