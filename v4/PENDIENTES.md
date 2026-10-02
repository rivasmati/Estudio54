# Pendientes de SEO · Estudio 54

Todo lo que se podía hacer en el código ya está aplicado (ver abajo). Esto es lo que depende de una respuesta o de un acceso externo.

## 1. Lo hace el estudio en Google Business Profile (necesita su cuenta)

Prioridad máxima: es lo que más pesa en "barbería cerca de mí".

- [ ] **Corregir horarios.** Hoy Google dice martes a jueves 10–21, viernes 11–21 y sábado 11–21:30. Cargar el horario real con dos franjas por día:
  - Lunes: cerrado
  - Martes a jueves: 11:00–15:30 y 17:00–19:00
  - Viernes: 11:00–15:30 y 17:00–20:30
  - Sábado: 11:00–17:00
  - Domingo: cerrado
- [ ] **Nombre:** dejar "Estudio 54" (hoy: "ESTUDIO 54 - Barbería y peluquería premium."). Las reglas de Google no permiten agregar descripciones al nombre.
- [ ] **Categorías:** principal "Barbería", sumar "Peluquería".
- [ ] **Dirección:** agregar "3° A".
- [ ] **Servicios con precio:** corte básico $20.000, corte + diseño $22.000, corte + barba $24.000.
- [ ] **Descripción:** texto listo en el plan de SEO.
- [ ] **Fotos:** 2 o 3 fotos de cortes por semana.
- [ ] **QR de reseñas** en el local (Google Business Profile → Pedir reseñas) y responder todas las reseñas.
- [ ] **Sitio web:** cambiar el link de Instagram por la web cuando esté publicada.

## 2. Datos a confirmar con el estudio

| Pregunta | Dónde se usa al confirmarla |
|---|---|
| ¿El horario real es el de la web? | `datos.json → horarios` (ya cargado con el horario que nos pasaron) |
| ¿Atienden sin turno? | Nueva pregunta frecuente en `datos.json → preguntas` |
| ¿Qué medios de pago aceptan? | Nueva pregunta frecuente + datos estructurados (`paymentAccepted`) |
| ¿Entre qué calles está el local? | Respuesta "¿Dónde queda?" y `llms.txt` |
| ¿Quieren mostrar el teléfono en la web? | Consistencia de datos con Google (hoy la web solo usa Instagram) |
| ¿De qué barrios vienen sus clientes? | Texto de la web (solo si es cierto) |
| ¿Sigue activa la cuenta @thebarber54_? | Si no se usa, que su bio derive a @54.estudio_ |
| ¿Aprueban la cinta "Barbería con oficio, en Flores"? | Texto del H1 (antes decía "Cortes con oficio, en Flores") |

## 3. Publicación (necesita dominio y hosting)

- [ ] Registrar el dominio (por ejemplo `estudio54.com.ar` en NIC Argentina).
- [ ] Completar `datos.json → sitio.url` con el dominio y correr `python3 build.py`. Eso genera solo `robots.txt`, `sitemap.xml`, la URL canónica y la imagen para compartir en WhatsApp.
- [ ] Subir `index.html`, `assets/`, `robots.txt`, `sitemap.xml` y `llms.txt` a la raíz del sitio.
- [ ] Dar de alta el sitio en Google Search Console y Bing Webmaster Tools y enviar el sitemap.
- [ ] Poner el link de la web en Google Maps, en la bio de Instagram y en Fresha.

## 4. Otros perfiles (necesitan las cuentas del estudio)

- [ ] Apple Business Connect (Apple Maps).
- [ ] Bing Places (se importa desde Google).
- [ ] Instagram: nombre de perfil "Estudio 54 · Barbería Flores", dirección en la bio y link a la web.
- [ ] Fresha: revisar que nombre, dirección y horarios coincidan con Google y la web.

## Ya aplicado en el código

- Título y meta descripción con "barbería", "peluquería", "Flores" y "CABA".
- H1 que dice qué es el negocio, dentro de la cinta roja (mismo aspecto visual).
- Datos estructurados schema.org (`HairSalon` + `FAQPage`): dirección, ubicación, horarios con la pausa, servicios con precio, barberos, link de reserva. Sin puntuación de reseñas, a propósito (Google no admite marcar reseñas de otra plataforma).
- Sección de preguntas frecuentes visible, generada desde `datos.json`.
- Texto alternativo descriptivo en las fotos de los servicios.
- `llms.txt` generado desde `datos.json`.
- `robots.txt`, `sitemap.xml`, URL canónica y `og:image` listos para generarse solos al completar el dominio.
- Precios en un solo lugar (`datos.json`): web, datos estructurados, preguntas y `llms.txt` se actualizan juntos.
