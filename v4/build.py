#!/usr/bin/env python3
"""Genera la landing de Estudio 54 a partir de la plantilla y los datos.

Entradas:
  src/index.html  plantilla con marcadores {{...}}
  datos.json      links, barberos y horarios (única fuente)
  assets/         imágenes

Salidas:
  index.html                 versión para publicar (imágenes en assets/)
  estudio54-landing-v4.html  archivo único con imágenes embebidas, para compartir

Uso:  python3 build.py
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIAS = {0: "Dom", 1: "Lun", 2: "Mar", 3: "Mié", 4: "Jue", 5: "Vie", 6: "Sáb"}
ORDEN = [1, 2, 3, 4, 5, 6, 0]  # la semana visible arranca el lunes


def minutos(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


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


def og_extra(datos):
    url = datos["sitio"].get("url", "").rstrip("/")
    if not url:
        return ""
    e = html.escape
    return (f'<meta property="og:url" content="{e(url)}/">\n'
            f'<meta property="og:image" content="{e(url)}/assets/logo.jpg">\n')


def render(plantilla, datos):
    a = lambda u: html.escape(u, quote=True)  # para usar dentro de href="..."
    b = datos["barberos"]
    valores = {
        "reserva": a(datos["links"]["reserva"]),
        "instagram": a(datos["links"]["instagram"]),
        "maps": a(datos["links"]["maps"]),
        "reserva_gonzalo": a(b["reserva_base"].format(id=b["gonzalo"]["employee_id"])),
        "reserva_danilo": a(b["reserva_base"].format(id=b["danilo"]["employee_id"])),
        "ig_gonzalo": a(b["gonzalo"]["instagram"]),
        "ig_danilo": a(b["danilo"]["instagram"]),
        "semana": semana_html(datos),
        "horarios_js": json.dumps({str(k): v for k, v in horarios(datos).items()}, separators=(",", ":")),
        "og_extra": og_extra(datos),
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
    print(f"index.html                 {len(pagina.encode()) // 1024} KB")
    print(f"estudio54-landing-v4.html  {len(unico.encode()) // 1024} KB (imágenes embebidas)")


if __name__ == "__main__":
    main()
