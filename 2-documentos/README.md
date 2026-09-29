# 2 — Documentos

Plantillas para CV, carta y emails. Son **plantillas**, no documentos listos para enviar:
nunca tienen tus datos reales.

## Estructura

```
2-documentos/
├── README.md
├── CV/
│   └── cv-plantilla.md       ← plantilla maestra
└── plantillas/
    ├── carta-presentacion.md
    ├── email-seguimiento.md
    ├── email-networking.md
    └── guia-de-estilo.md     ← cómo escribes tú
```

## La regla de las plantillas

Ninguna plantilla lleva datos reales. Todo lo que es tuyo va en el momento de usarla, o
en `1-perfil-profesional/`, que es la fuente de verdad.

Las plantillas usan marcadores entre corchetes:

```
[TU_NOMBRE]
[TU_PUESTO_OBJETIVO]
[MODALIDAD]
[TIPO_DE_CONTRATO]
[EMPRESA]
[TU_EMAIL]
```

Busca `[` y reemplaza. Si queda alguno sin cambiar, el documento está mal.

## La guía de estilo

`plantillas/guia-de-estilo.md` es el archivo más útil de esta carpeta, y el más ignorado.

Un CV o una carta no tienen que sonar como cualquier otro. Si todos dicen "apasionado",
"motivado" y "gusto por el aprendizaje", ninguno destaca. Escribir con tu voz real es lo
que te separa del resto del montón.

Rellénala una vez, con ejemplos de cómo escribes tú de verdad, y úsala cada vez que
generes un documento.

## Flujo por candidatura

1. Copia `plantillas/carta-presentacion.md` a `5-postulaciones/AAAA-MM-DD_EMPRESA_PUESTO/`.
2. Rellena desde `1-perfil-profesional/`, no de memoria.
3. Ajusta el titular al puesto concreto.
4. Cita 1-2 logros del `banco-de-logros.md`, no los mismos en todas.
5. Lee en voz alta. Si suena a nadie, reescribe.

## Verificación antes de enviar

- [ ] No queda ningún marcador `[...]` sin sustituir
- [ ] El titular menciona el puesto exacto, no "el puesto"
- [ ] Cada afirmación del CV tiene respaldo en `1-perfil-profesional/`
- [ ] No hay frases que no dirías en una entrevista
- [ ] No hay datos de otra candidatura anterior (nombre de otra empresa)
- [ ] Has decidido conscientemente si incluyes teléfono y email (ver `PRIVACY.md`)
