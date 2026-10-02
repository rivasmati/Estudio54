# Estudio 54 · Reglas de diseño (v4)

Combinación de la v1 (calidez: dorado, tono cercano) y la v2 (carácter de barbería: tipografía de cartel, poste).

## Color
| Token | Valor | Uso permitido |
|---|---|---|
| `--night` | #0B0E14 | Fondo único de toda la página |
| `--night-2` | #131823 | Tarjetas sobre oscuro |
| `--ink` | #12151C | Texto sobre botones blancos |
| `--white` | #F5F3EE | Texto sobre oscuro |
| `--red` | #C8323A | **Solo** botones de acción, la cinta del hero, el poste y el panel de cierre (texto rojo sobre oscuro: #FF7A80) |
| `--blue` | #2F5BD3 / `--blue-light` #86A3F2 | **Solo** etiquetas de sección y el poste |
| `--gold` | #CDA85F | **Solo** logo, sello, estrellas y precios |

Contraste mínimo 4.5:1 en todo el texto.

## Tipografía
- **Barlow Condensed** (700–900), siempre en MAYÚSCULAS: títulos, botones, etiquetas, nombres, precios.
- **Barlow** (400–600): todo el texto corrido. Base 17px, interlineado 1.55.
- Escala: 14 · 16 · 18 · 24 · 32 · 48 · 72 · 112.
- Prohibido: serif itálica, emojis como íconos.

## Forma
- Un solo radio: **6px** (botones, tarjetas, fotos, mapa).
- Sin sombras ni brillos. Las tarjetas se separan con un borde de 1px.
- Fotos siempre derechas (sin inclinar) y sin stickers encima.

## Ritmo
- **Un solo fondo** para toda la página (`--night`). Sin secciones de otro color de borde a borde: los saltos de brillo al scrollear marean.
- Las secciones se separan con espacio (72px escritorio / 48px celular) y con su etiqueta azul + título, no con color.
- Las tarjetas usan `--night-2`, un tono apenas más claro, para distinguirse sin generar saltos.
- El cierre es un **panel** rojo dentro de la página, no una franja de borde a borde.
- El **poste de barbero** aparece solo junto a la foto del hero.
- Espaciado en múltiplos de 8.
- Cada sección empieza igual: etiqueta azul → título → bajada opcional, alineados a la izquierda.

## Encabezado
- Uno solo, fijo, compacto: 64px en escritorio y 56px en celular.
- Siempre muestra logo + **estado en vivo** (abierto / pausa / cerrado), que lleva a los horarios.
- En escritorio suma el menú y "Reservar"; en celular "Reservar" vive solo en la barra de abajo.

## Componentes
- **Botón primario:** fondo rojo, texto blanco. **Secundario:** contorno del color del texto. Alto 52px (44px chico).
- **Interacción:** hover de 200ms; foco visible dorado; se respeta `prefers-reduced-motion`.
- **Móvil:** un solo "Reservar" (la barra fija de abajo); el del encabezado se oculta.

## Contenido
- Siempre "Estudio 54", nunca "el 54".
- Contacto solo por Instagram (sin WhatsApp ni teléfono).
- Partido y charla/amor: solo en "Buen ambiente" y en las reseñas. LGBTQ+: solo en el footer.
- Fotos de cortes en todos lados, salvo el equipo (retratos) y los reels (videos divertidos).
- Reseñas: todas con la misma jerarquía.
