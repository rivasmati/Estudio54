# Estudio 54 · Reglas de diseño (v4)

Combinación de la v1 (calidez: crema, dorado) y la v2 (carácter de barbería: tipografía de cartel, poste).

## Color
| Token | Valor | Uso permitido |
|---|---|---|
| `--night` | #0B0E14 | Fondo de secciones oscuras |
| `--night-2` | #131823 | Tarjetas sobre oscuro |
| `--cream` | #F2EBDD | Fondo de secciones claras |
| `--paper` | #FBF8F2 | Tarjetas sobre crema |
| `--ink` | #12151C | Texto sobre crema |
| `--white` | #F5F3EE | Texto sobre oscuro |
| `--red` | #C8323A | **Solo** botones de acción, la cinta del hero, el poste y el bloque final |
| `--blue` | #2F5BD3 / `--blue-light` #86A3F2 | **Solo** etiquetas de sección y el poste |
| `--gold` | #CDA85F / `--gold-deep` #8A6A2E (sobre crema) | **Solo** logo, sello, estrellas y precios |

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
- Secciones alternadas estrictamente: oscuro → crema → oscuro → crema…; el cierre va en rojo.
- El **poste de barbero** aparece solo en tres lugares: junto a la foto del hero y como franja debajo del hero y arriba del footer.
- Espaciado en múltiplos de 8. Padding de sección: 96px (escritorio) / 64px (celular).
- Cada sección empieza igual: etiqueta azul → título → bajada opcional, alineados a la izquierda.

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
