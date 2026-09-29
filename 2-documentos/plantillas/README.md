# Plantillas

Plantillas de documentos que genera o adapta cada persona. Sin datos reales, por diseño.

## Archivos

| Archivo | Para qué sirve |
|---------|----------------|
| `guia-de-estilo.md` | **Empieza por aquí.** Cómo escribes tú: tono, frases que usas, frases que evitas, ejemplos |
| `carta-presentacion.md` | Carta de presentación para una candidatura concreta |
| `email-seguimiento.md` | Recordatorio cuando no recibes respuesta |
| `email-networking.md` | Mensajes en frío y seguimiento de contactos |

## La guía de estilo va primero

Los otros tres archivos son plantillas de estructura: dicen qué secciones tener, no qué
tono usar. El tono lo pones tú en `guia-de-estilo.md`, y es lo que hace que una carta no
suene a las otras 400 que llegan esa semana.

Un agente de IA que genera tu carta está obligado a leer la guía de estilo antes (ver
`AGENTS.md` en la raíz). Si le escribes solo la plantilla de carta, te va a escribir como
se escribe en general: correcto y anónimo.

## Marcadores

Todas las plantillas usan marcadores entre corchetes:

```
[TU_NOMBRE]
[EMPRESA]
[PUESTO_EXACTO]
[LOGRO_CON_CIFRA]
```

**Regla:** antes de enviar cualquier documento, busca `[` en el fichero. Si aparece algo
entre corchetes que no sea un enlace, el documento no está listo.

Los marcadores son deliberadamente genéricos para que el repo sea reutilizable. No los
completes en la plantilla: complétalos en la copia que uses.

## Formato de trabajo por candidatura

```
5-postulaciones/AAAA-MM-DD_EMPRESA_PUESTO/
├── oferta.md        ← la oferta original, guardada
├── cv-enviado.*     ← el CV que mandaste (ignorado por git)
├── carta.md         ← la carta que mandaste
└── seguimiento.md   ← notas y recordatorios
```

Esa carpeta es tu historial. `5-postulaciones/` está en `.gitignore` salvo la carpeta
`EJEMPLO_`, precisamente porque contiene datos que no deben subirse. Ver `PRIVACY.md`.
