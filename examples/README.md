# Ejemplos

Un recorrido completo con datos inventados: perfil, dos ofertas y una
postulación.

Sirve para dos cosas:

1. Ver el resultado antes de rellenar nada, y saber qué se espera de cada
   fichero.
2. Comprobar que el repo funciona con datos de otra persona sin mezclarlos con
   los tuyos.

## Estructura

```
examples/perfil-ficticio/
├── 1-perfil-profesional/
│   ├── experiencia.md
│   ├── formacion.md
│   ├── habilidades.md
│   └── banco-de-logros.md
├── 4-ofertas/
│   ├── pipeline.example.csv
│   └── plantilla-oferta.llena.md
└── 5-postulaciones/
    └── EJEMPLO_Empresa_Ficticia/
        ├── README.md
        ├── oferta.md
        ├── carta.md
        └── notas.md
```

Sigue la numeración de la raíz a propósito: el ejemplo tiene el mismo orden que
el repo, así que se ven las equivalencias.

## Los datos

Son ficticios. Cualquier parecido con una persona real es casualidad.

- Nombre: **Ejemplo Ficticio**. Nunca un nombre real, ni siquiera de ejemplo.
- Empresas: `Empresa Ficticia SL`, `Consultora Ficticia`.
- URLs: `https://example.com/...`. `example.com` está reservado para esto.
- Contactos: `contacto@ejemplo.com`.
- Fechas: de 2026, para que no coincidan con nada tuyo.

## Por qué el perfil se llama así

Porque si se llamara `lucia-martinez/` habría dos problemas: alguien podría
confundirse creyendo que es real, y el escáner de privacidad empezaría a dar
falsos positivos con cada nombre que añadiras al tuyo.

## Cómo usarlo

Copia el perfil ficticio a `1-perfil-profesional/` como punto de partida, borra
todo y escribe lo tuyo. La estructura te queda gratis.

```bash
# Linux y WSL
cp -r examples/perfil-ficticio/1-perfil-profesional/* 1-perfil-profesional/

# Windows PowerShell
Copy-Item -Recurse -Force examples\perfil-ficticio\1-perfil-profesional\* 1-perfil-profesional\
```

O cópialo a otro sitio y míralo sin prisa. Está aquí para eso.

## Lo que no hay

Deliberadamente:

- Ningún email ni teléfono real
- Ninguna empresa real
- Ninguna cifra real
- Ninguna URL que exista
- Ningún nombre de persona real

Si añades algo de eso, `check-privacidad.py` va a fallar, y va a tener razón.
