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

## Cómo editar la v4

La v4 se genera a partir de una plantilla y un archivo de datos:

| Archivo | Qué contiene |
|---|---|
| `v4/datos.json` | **Única fuente** de links (Fresha, Instagram, Maps), IDs de Fresha de cada barbero y horarios. |
| `v4/src/index.html` | Plantilla de la página (textos, estructura y estilos). |
| `v4/build.py` | Genera `index.html` y `estudio54-landing-v4.html`. |

Después de editar `datos.json` o `src/index.html`:

```bash
cd v4
python3 build.py
```

No edites `v4/index.html` ni `v4/estudio54-landing-v4.html` a mano: se sobrescriben en cada build.

### Qué archivo usar
- **Para publicar en un hosting:** `index.html` + `assets/`. Las imágenes se cargan aparte y de forma diferida, así la página abre más rápido.
- **Para mandar por WhatsApp o mail:** `estudio54-landing-v4.html`, que tiene todo adentro. Pesa unos 650 KB porque las imágenes van embebidas.

### Vista previa al compartir el link
Las etiquetas Open Graph de título y descripción ya están. Para que WhatsApp muestre también la imagen, completá `sitio.url` en `datos.json` con la URL pública y volvé a correr el build.

## Datos

Precios, reseñas, puntuación y seguidores están cargados a mano en la plantilla. Los horarios están en `datos.json`: con ellos se arma la semana visible y se calcula el estado abierto/pausa/cerrado, que se actualiza cada minuto con la hora de Buenos Aires.

Los links "Reservar con Gonzalo/Danilo" usan el `employee_id` interno de Fresha. Si un barbero se da de baja o se vuelve a registrar, hay que actualizar su ID en `datos.json` (ver la nota en ese archivo).
