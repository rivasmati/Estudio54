# Estudio54

Propuesta de landing page para **Estudio 54**, barbería y peluquería en Flores (CABA). Unifica en una sola página lo que hoy está repartido entre Instagram, Google Maps y Fresha: servicios y precios, equipo, reseñas, videos, horarios, ubicación y reserva online.

## Versiones

| Carpeta | Descripción |
|---|---|
| `v1/` | Primera versión: negro, crema y dorado, tono descontracturado. |
| `v2/` | Estructura nueva con estilo barbería: rojo, blanco y azul, tipografía de cartel y poste animado. |
| `v3/` | Estilo de la v1 con el contenido y las reglas de la v2. |
| `v4/` | **Versión actual.** Combina v1 y v2 con un sistema de diseño fijo (ver [`v4/DISENO.md`](v4/DISENO.md)). |

Cada carpeta tiene:
- `index.html` + `assets/`: versión editable.
- `estudio54-landing*.html`: archivo único con las imágenes embebidas, para compartir y abrir directo en el navegador.

## Ver localmente

```bash
python3 -m http.server 5454
```

Y abrir `http://localhost:5454/v4/`.

## Datos

Horarios, precios, reseñas y puntuación están cargados a mano en el HTML. El estado abierto/pausa/cerrado se calcula en vivo con la hora de Buenos Aires a partir de esos horarios.
