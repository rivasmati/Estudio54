#!/usr/bin/env python3
"""Genera la landing de Estudio 54 a partir de la plantilla y los datos.

Entradas:
  src/index.html  plantilla con marcadores {{...}}
  datos.json      datos del negocio (única fuente)
  assets/         imágenes

Salidas:
  index.html                 versión para publicar (imágenes en assets/)
  estudio54-landing-v4.html  archivo único con imágenes embebidas, para compartir
  llms.txt                   resumen del negocio para asistentes de IA
  robots.txt, sitemap.xml    solo cuando datos.json → sitio.url tiene el dominio

Uso:  python3 build.py
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIAS = {0: "Dom", 1: "Lun", 2: "Mar", 3: "Mié", 4: "Jue", 5: "Vie", 6: "Sáb"}
DIAS_LARGOS = {0: "domingo", 1: "lunes", 2: "martes", 3: "miércoles", 4: "jueves", 5: "viernes", 6: "sábado"}
DIAS_SCHEMA = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
ORDEN = [1, 2, 3, 4, 5, 6, 0]  # la semana visible arranca el lunes
SERVICIOS = ["basico", "diseno", "barba"]


# ---------- utilidades ----------

def minutos(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def pesos(n):
    """20000 → '$20.000' (formato argentino)."""
    return "$" + f"{n:,}".replace(",", ".")


def sitio_url(datos):
    return datos["sitio"].get("url", "").strip().rstrip("/")


def horarios(datos):
    """Devuelve {día: [[inicio, fin], ...]} en minutos, validando el formato."""
    out = {}
    for k, turnos in datos["horarios"].items():
        if k.startswith("_"):
            continue
        dia = int(k)
        franjas = []
        for inicio, fin in turnos:
            a, b = minutos(inicio), minutos(fin)
            if a >= b:
                raise ValueError(f"Turno inválido el día {DIAS[dia]}: {inicio}-{fin}")
            franjas.append([a, b])
        out[dia] = sorted(franjas)
    faltan = set(DIAS) - set(out)
    if faltan:
        raise ValueError(f"Faltan días en datos.json → horarios: {sorted(faltan)}")
    if not any(out.values()):
        # El cálculo de "próxima apertura" en el navegador necesita al menos un día abierto.
        raise ValueError("datos.json → horarios: tiene que haber al menos un día con turnos")
    return out


def horarios_texto(datos):
    """Horario en una frase, agrupando días seguidos con el mismo horario."""
    grupos = []
    for dia in ORDEN:
        turnos = tuple(tuple(t) for t in datos["horarios"][str(dia)])
        if grupos and grupos[-1][1] == turnos:
            grupos[-1][0].append(dia)
        else:
            grupos.append(([dia], turnos))
    partes = []
    for dias, turnos in grupos:
        nombre = DIAS_LARGOS[dias[0]] if len(dias) == 1 else f"{DIAS_LARGOS[dias[0]]} a {DIAS_LARGOS[dias[-1]]}"
        if turnos:
            franjas = " y ".join(f"de {a} a {b}" for a, b in turnos)
            partes.append(f"{nombre.capitalize()} {franjas}.")
        else:
            partes.append(f"{nombre.capitalize()} cerrado.")
    return " ".join(partes)


def precios_texto(datos):
    """'El corte básico sale $20.000, el corte + diseño $22.000 y el corte + barba $24.000.'"""
    s = datos["servicios"]
    items = [f"el {s[k]['nombre'].lower()} {pesos(s[k]['precio'])}" for k in SERVICIOS]
    items[0] = items[0].replace(" $", " sale $", 1)
    return (", ".join(items[:-1]) + " y " + items[-1] + ".").capitalize()


def preguntas(datos):
    reemplazos = {"{precios}": precios_texto(datos), "{horarios}": horarios_texto(datos)}
    lista = []
    for item in datos["preguntas"]["lista"]:
        r = item["r"]
        for k, v in reemplazos.items():
            r = r.replace(k, v)
        lista.append((item["p"], r))
    return lista


# ---------- piezas de la página ----------

def semana_html(datos):
    filas = []
    for dia in ORDEN:
        turnos = datos["horarios"][str(dia)]
        if turnos:
            items = "".join(f"<li>{a} – {b}</li>" for a, b in turnos)
            filas.append(f'      <div class="day" data-d="{dia}"><h3>{DIAS[dia]}</h3><ul>{items}</ul></div>')
        else:
            filas.append(f'      <div class="day off" data-d="{dia}"><h3>{DIAS[dia]}</h3><ul><li>Cerrado</li></ul></div>')
    return "\n".join(filas)


def faq_html(datos):
    e = html.escape
    return "\n".join(
        f'      <details><summary>{e(p)}</summary><p>{e(r)}</p></details>' for p, r in preguntas(datos)
    )


def og_extra(datos):
    url = sitio_url(datos)
    if not url:
        return ""
    e = html.escape
    return (f'<meta property="og:url" content="{e(url)}/">\n'
            f'<meta property="og:image" content="{e(url)}/assets/logo.jpg">\n'
            f'<link rel="canonical" href="{e(url)}/">\n')


def schema(datos):
    """Datos estructurados schema.org (JSON-LD). Solo marca lo que es visible en la página."""
    s, b, url = datos["sitio"], datos["barberos"], sitio_url(datos)
    h = datos["horarios"]

    # Agrupa días con el mismo turno para openingHoursSpecification
    franjas = {}
    for dia in range(7):
        for a, c in h[str(dia)]:
            franjas.setdefault((a, c), []).append(DIAS_SCHEMA[dia])
    apertura = [{"@type": "OpeningHoursSpecification", "dayOfWeek": d if len(d) > 1 else d[0], "opens": a, "closes": c}
                for (a, c), d in sorted(franjas.items(), key=lambda x: (x[0][0], x[0][1]))]

    negocio = {
        "@type": "HairSalon",
        "name": "Estudio 54",
        "description": "Barbería y peluquería en Flores, CABA. Cortes de pelo, fades, diseños y perfilado de barba con turno online.",
        "priceRange": f"ARS {pesos(min(datos['servicios'][k]['precio'] for k in SERVICIOS))[1:]} – {pesos(max(datos['servicios'][k]['precio'] for k in SERVICIOS))[1:]}",
        "currenciesAccepted": "ARS",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s["direccion"],
            "addressLocality": s["ciudad"],
            "addressRegion": "CABA",
            "postalCode": s["codigo_postal"],
            "addressCountry": "AR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lng"]},
        "hasMap": datos["links"]["maps"],
        "openingHoursSpecification": apertura,
        "sameAs": [datos["links"]["instagram"], datos["links"]["maps"], s["fresha_perfil"]],
        "potentialAction": {"@type": "ReserveAction", "name": "Reservar turno", "target": datos["links"]["reserva"]},
        "employee": [
            {"@type": "Person", "name": b[k]["nombre"], "jobTitle": b[k]["puesto"], "sameAs": b[k]["instagram"]}
            for k in ("gonzalo", "danilo")
        ],
        "makesOffer": [
            {"@type": "Offer", "price": str(datos["servicios"][k]["precio"]), "priceCurrency": "ARS",
             "itemOffered": {"@type": "Service", "name": datos["servicios"][k]["nombre"],
                             "description": datos["servicios"][k]["descripcion"]}}
            for k in SERVICIOS
        ],
    }
    if url:
        negocio.update({"@id": f"{url}/#negocio", "url": f"{url}/",
                        "image": f"{url}/assets/logo.jpg", "logo": f"{url}/assets/logo.jpg"})

    faq = {
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}}
                       for p, r in preguntas(datos)],
    }
    data = {"@context": "https://schema.org", "@graph": [negocio, faq]}
    # "</" escapado para que el JSON no pueda cerrar la etiqueta <script>
    cuerpo = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{cuerpo}\n</script>'


def render(plantilla, datos):
    a = lambda u: html.escape(u, quote=True)  # para usar dentro de href="..."
    b = datos["barberos"]
    sv = datos["servicios"]
    valores = {
        "reserva": a(datos["links"]["reserva"]),
        "instagram": a(datos["links"]["instagram"]),
        "maps": a(datos["links"]["maps"]),
        "reserva_gonzalo": a(b["reserva_base"].format(id=b["gonzalo"]["employee_id"])),
        "reserva_danilo": a(b["reserva_base"].format(id=b["danilo"]["employee_id"])),
        "ig_gonzalo": a(b["gonzalo"]["instagram"]),
        "ig_danilo": a(b["danilo"]["instagram"]),
        "precio_basico": pesos(sv["basico"]["precio"]),
        "precio_diseno": pesos(sv["diseno"]["precio"]),
        "precio_barba": pesos(sv["barba"]["precio"]),
        "precio_desde": pesos(min(sv[k]["precio"] for k in SERVICIOS)),
        "semana": semana_html(datos),
        "faq": faq_html(datos),
        "horarios_js": json.dumps({str(k): v for k, v in horarios(datos).items()}, separators=(",", ":")),
        "og_extra": og_extra(datos),
        "schema": schema(datos),
    }
    usados = set(re.findall(r"\{\{(\w+)\}\}", plantilla))
    faltan = usados - set(valores)
    if faltan:
        raise KeyError(f"Marcadores sin valor: {sorted(faltan)}")
    salida = re.sub(r"\{\{(\w+)\}\}", lambda m: valores[m.group(1)], plantilla)
    return salida.replace(
        "<!-- PLANTILLA: no editar index.html directamente. Editar src/index.html y datos.json, y correr: python3 build.py -->",
        "<!-- ARCHIVO GENERADO por build.py: editar src/index.html y datos.json, no este archivo. -->",
    )


# ---------- archivos de SEO ----------

def llms_txt(datos):
    s, sv, b = datos["sitio"], datos["servicios"], datos["barberos"]
    url = sitio_url(datos)
    lineas = [
        "# Estudio 54", "",
        f"> Barbería y peluquería en {s['barrio']}, {s['ciudad']}, Argentina.",
        "> Cortes de pelo, fades, diseños y perfilado de barba. Turnos online.", "",
        "## Servicios y precios (ARS)",
    ]
    lineas += [f"- {sv[k]['nombre']}: ARS {pesos(sv[k]['precio'])[1:]}. {sv[k]['duracion'].capitalize()}. {sv[k]['descripcion']}"
               for k in SERVICIOS]
    lineas += ["Precios de referencia; se confirman al reservar.", "", "## Barberos"]
    lineas += [f"- {b[k]['nombre']}: {b[k]['puesto'].lower()}. Instagram: {b[k]['instagram']}" for k in ("gonzalo", "danilo")]
    lineas += ["", "## Horarios"]
    for dia in ORDEN:
        turnos = datos["horarios"][str(dia)]
        valor = " y ".join(f"{a} a {c}" for a, c in turnos) if turnos else "cerrado"
        lineas.append(f"- {DIAS_LARGOS[dia].capitalize()}: {valor}")
    lineas += ["", "## Dirección",
               f"{s['direccion']}, {s['barrio']} ({s['codigo_postal']}), {s['ciudad']}, Argentina.",
               f"Google Maps: {datos['links']['maps']}", "",
               "## Reservas y contacto",
               f"- Turnos online (Fresha): {datos['links']['reserva']}",
               f"- Instagram (consultas por mensaje directo): {datos['links']['instagram']}"]
    if url:
        lineas += ["", "## Sitio", f"- Inicio: {url}/"]
    return "\n".join(lineas) + "\n"


def robots_txt(url):
    bots = ["*", "Googlebot", "Bingbot", "Google-Extended", "Applebot-Extended",
            "ClaudeBot", "GPTBot", "OAI-SearchBot", "PerplexityBot"]
    cuerpo = "\n\n".join(f"User-agent: {b}\nAllow: /" for b in bots)
    return ("# Estudio 54: acceso abierto a buscadores y asistentes de IA para que lean\n"
            "# correctamente horarios, servicios, precios y ubicación.\n\n"
            f"{cuerpo}\n\nSitemap: {url}/sitemap.xml\n")


def sitemap_xml(url):
    from datetime import date
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'  <url>\n    <loc>{html.escape(url)}/</loc>\n    <lastmod>{date.today().isoformat()}</lastmod>\n  </url>\n'
            '</urlset>\n')


def embeber_imagenes(pagina):
    """Reemplaza src/href a assets/*.jpg por data URIs (cada imagen se codifica una sola vez)."""
    cache = {}

    def data_uri(ruta):
        if ruta not in cache:
            cache[ruta] = "data:image/jpeg;base64," + base64.b64encode((ROOT / ruta).read_bytes()).decode()
        return cache[ruta]

    return re.sub(r'(src|href)="(assets/[^"]+\.jpg)"', lambda m: f'{m.group(1)}="{data_uri(m.group(2))}"', pagina)


def main():
    datos = json.loads((ROOT / "datos.json").read_text(encoding="utf-8"))
    plantilla = (ROOT / "src" / "index.html").read_text(encoding="utf-8")
    pagina = render(plantilla, datos)
    (ROOT / "index.html").write_text(pagina, encoding="utf-8")
    unico = embeber_imagenes(pagina)
    (ROOT / "estudio54-landing-v4.html").write_text(unico, encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms_txt(datos), encoding="utf-8")
    print(f"index.html                 {len(pagina.encode()) // 1024} KB")
    print(f"estudio54-landing-v4.html  {len(unico.encode()) // 1024} KB (imágenes embebidas)")
    print("llms.txt                   listo")

    url = sitio_url(datos)
    if url:
        (ROOT / "robots.txt").write_text(robots_txt(url), encoding="utf-8")
        (ROOT / "sitemap.xml").write_text(sitemap_xml(url), encoding="utf-8")
        print(f"robots.txt, sitemap.xml    listos para {url}")
    else:
        for f in ("robots.txt", "sitemap.xml"):
            (ROOT / f).unlink(missing_ok=True)
        print("robots.txt, sitemap.xml    PENDIENTES: completar sitio.url en datos.json con el dominio")


if __name__ == "__main__":
    main()
