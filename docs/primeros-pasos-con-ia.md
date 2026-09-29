# Cómo trabajar con IA en este repo

Antes de nada: esto es un repo de documentos. Una IA ayuda a ordenar ideas, pulir
textos y mirar que no se te escape nada. No sabe nada de tu experiencia, y no puede
inventarla. Esa es la regla que ordena todo lo demás.

## Las tres reglas

### 1. La IA no escribe tu CV. Tú sí.

`1-perfil-profesional/` es la fuente de verdad. La IA puede:
- hacerte preguntas para vaciar lo que sabes
- ordenar, resumir, cortar frases largas
- sugerir palabras clave a partir de ofertas reales
- señalar huecos: "aquí no hay nada que contar"
- revisar que el CV y LinkedIn digan lo mismo

La IA no puede:
- inventar un logro, una cifra, una tecnología
- convertir "ayudé con" en "lideré"
- rellenar un año que no sabes
- rellenar un puesto que no exercias

La diferencia entre "ayudé a migrar" y "migré" es pequeña en el texto y enorme en una
entrevista. La IA no sabe esa diferencia. Tú sí.

### 2. Una pregunta cada vez

No le digas "me haz un CV, una carta y un plan de búsqueda". Va a inventar cosas
para llenar huecos, y con estilo además.

Pregunta una cosa:

> ¿Qué es lo que haces en este puesto, en una frase, sin adjetivos?

Y cuando respondes, sigue. El contexto se acumula solo.

### 3. Nada de datos personales en un prompt

Ni tu email, ni tu teléfono, ni tu dirección, ni el nombre real de una empresa donde
trabajaste, ni capturas de tu LinkedIn.

Por dos razones: se quedan en el historial del proveedor, y no estás dentro de un
repo. Cuando trabajes con un documento, pega solo el fragmento que necesites.

## Forma de trabajar

### Empezar de cero

1. Abre `1-perfil-profesional/README.md` y rellena lo que ya tengas a mano.
2. Sesión con IA, una pregunta cada vez: experiencia, formación, habilidades, logros.
3. Revisa la carpeta de arriba abajo. Quita lo que no puedas sostener.
4. Solo entonces empieza el CV.

### Al tailoring de una oferta concreta

1. Copia la oferta en `4-ofertas/` y complétala con `plantilla-oferta.md`.
2. Pide a la IA que compare la oferta con tu `habilidades.md` y te diga qué pedir
   a hacer. En la columna `Encaje`, cada dimensión con un número y una nota.
3. Pide dos versiones de las frases de los puntos que tocan el puesto.
4. Elige tú. La versión buena es la que puedes defender en la entrevista.

## Prompts que funcionan

**Extraer logros de un descripción de puesto:**

> Aquí tienes las tareas de un puesto. Sin inventar nada, dime qué preguntas tendría
> que poder responder alguien que hubiera hecho ese trabajo, para saber si encajo.
> No me digas qué experiencia tengo: dime qué tendría que demostrar.

**Criticar un CV sin suavizarlo:**

> Lee este CV como wouldn uno que es un reclutador escéptico y con prisa. Dime
> cinco cosas concretas por las que descartaría a esta persona. No seas amable.

**Verificar coherencia:**

> Compara mi CV y mi LinkedIn. Dime qué afirmaciones no coinciden y cuál de los dos
> documentos está más desactualizado.

**Aclarar un perfil:**

> Este puesto pide diez cosas. De mi perfil, ¿cuáles puedo demostrar con un ejemplo
> concreto y cuáles no? Para las que no, dime qué me faltaría.

## Qué mirar siempre antes de enviar nada

| Comprueba | Por qué |
|----------|---------|
| ¿Cada cifra es real? | Es lo primero que preguntan |
| ¿Cada technology la he usado? | Una entrevista la descubre en dos minutos |
| ¿El verbo refleja lo que hice yo? | "Lideré" y "colaboré" no son lo mismo |
| ¿El CV y LinkedIn cuentan lo mismo? | Si no, preguntan por la diferencia |
| ¿Hay algo que no pueda explicar? | Si no lo puedes explicar, no debería estar |

## Configurar una IA para este repo

Si tu herramienta lee `AGENTS.md` o `CLAUDE.md` (este repo tiene ambos en la raíz),
ya tiene contexto. Si no, pega esto al empezar:

> Trabaja en un repo de búsqueda de empleo. `1-perfil-profesional/` es la fuente de
> verdad. No inventes experiencia, cifras ni tecnologías. Una pregunta cada vez.
> Nada de datos personales: usa marcadores como `[TU_NOMBRE]`. Nada de enviar
> candidaturas ni automatizar portales de empleo.

## Lo que la IA no puede hacer

- No puede saber qué hizo nadie en un trabajo que no está escrito.
- No puede sustituir una revisión de la ortografía de tu versión en tu idioma.
- No puede saber qué empresa te conviene a ti.
- No puede garantizar que un CV pase un filtro automático.
- No puede hablar por ti en una entrevista.

Para eso están los datos de `1-perfil-profesional/`: porque la parte que
necesitas de verdad no se puede generar. Se recuerda.
