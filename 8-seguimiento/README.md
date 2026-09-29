# 8. Seguimiento

La parte que más se abandona y la que más resultados da.

## Las reglas

1. **Un seguimiento por candidatura, con fecha.** No "ya lo haré".
2. **Si no hay fecha en el pipeline, no hay seguimiento.** Solo una intención.
3. **Tres intentos y se cierra.** Dos emails y una llamada. Después, `SinRespuesta`.
4. **Cada respuesta se registra el mismo día.** Lo que no se anota, se olvida.

## Los tiempos

| Situación | Cuándo actuar |
|-----------|---------------|
| Enviada, sin respuesta | A los 7-10 días, un email |
| Sin respuesta tras el primer email | A los 10-14 días, un segundo email |
| Sin respuesta tras dos emails | Una llamada. Si no, se cierra |
| Dijeron "te avisamos", y pasaron 3 semanas | Un email: "quería confirmar si sigue abierta" |
| Entrevista programmerada | El día antes, confirmar |
| Prueba técnica recibida | En 24-48 h, un agradecimiento |
| Entrevista hecha | En 24 h, un agradecimiento con algo concreto |
| Sin noticias tras una entrevista | A los 7 días |
| Oferta recibida | En 48 h, por escrito, aunque aceptes en el momento |

`ver-ofertas.py` agrupa las ofertas por lo que necesitan de ti, usando la columna
`FechaSeguimiento` del pipeline. Pon la fecha ahí y no pienses más en ello.

## Qué dice un seguimiento

Cinco líneas. Ni seis, ni cero.

```
Asunto: [EMPRESA] - [PUESTO]

Hola [NOMBRE]:

Escribo por mi candidatura del [FECHA] para [PUESTO]. Envié el CV el [FECHA]
y no he tenido noticias.

Me sigue interesando el puesto, y si el proceso está en pausa por mi lado,
decímelo y lo dejamos así sin problema.

Gracias,
[TU_NOMBRE]
```

Lo que hace bien: es corto, no reclama, y le da salida digna. Nadie quiere
contestar a un email que suena a queja.

## Qué no hacer

- **"Quedo a la espera"** como email entero.
- Adjuntar otra vez el CV sin que te lo pidan.
- Reenviar el email original con "reenviado" arriba.
- Escribir el tercer email. A partir de ahí es ruido, y lo sabes.

## El pipeline

`ver-ofertas.py` te muestra cuatro grupos:

| Grupo | Qué hacer |
|-------|-----------|
| Seguimientos atrasados | Hoy, sin excepción |
| Seguimientos de esta semana | Con tiempo |
| Enviadas sin respuesta hace más de 3 semanas | Decide: escribir o cerrar |
| Interesantes sin preparar | O las preparas o las descartas |

El último grupo es el que más se ignora y el que más dinero cuesta: una oferta
marcada `Interesante` sin carta ni CV ajustado es una oportunidad que se enfría
mientras decides.

## Cerrar

Cuando dejas de seguir, cambia el estado a `SinRespuesta` o `Descartada` y
ponle una nota. Cerrar es una decisión; dejar filas en `Enviada` para siempre es
solo ruido.

Y si hubo una entrevista que salió mal, escribe dos líneas de por qué. La misma
razón aparece en la cuarta entrevista.
