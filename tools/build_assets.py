#!/usr/bin/env python3
"""Generates the profile SVGs in ../assets (banner, architecture, divider).

Every asset is emitted in a -dark and a -light variant from the same layout,
so both themes always stay in sync. `architecture.svg` is an extra adaptive
copy that switches palette with prefers-color-scheme when opened on its own.

Text is localized through STRINGS: English writes `<name>-<mode>.svg` (used by
README.md), Portuguese writes `<name>-pt-BR-<mode>.svg` (used by README.pt-BR.md).

Constraints for GitHub rendering: no <script>, no external fonts or images;
animation uses SMIL / CSS only and is disabled under prefers-reduced-motion.

Usage: python3 tools/build_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "Inter, 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

PALETTES = {
    "dark": {
        "bg": "#0A1628", "panel": "#0E1F38", "grid": "#16304F", "grid2": "#1D3D63",
        "line": "#2A5A8F", "primary": "#0070F2", "primary_text": "#4DA3FF",
        "accent": "#22D3EE", "text": "#E6EEF8", "muted": "#8BA3C1",
        "node": "#0F2240", "node_stroke": "#24497A", "core": "#0B2A55",
        "chip_text": "#FFFFFF",
    },
    "light": {
        "bg": "#F4F8FE", "panel": "#FFFFFF", "grid": "#E1EBF7", "grid2": "#CCDCF0",
        "line": "#8DB3E2", "primary": "#0070F2", "primary_text": "#0062D6",
        "accent": "#0891B2", "text": "#0A1628", "muted": "#4A6382",
        "node": "#FFFFFF", "node_stroke": "#B9CFEA", "core": "#EAF2FE",
        "chip_text": "#FFFFFF",
    },
}

# Localized copy. Keys are shared by every language; "en" is the default.
STRINGS = {
    "en": {
        "banner_title": "João Victor R. V. Godoi — SAP Developer",
        "banner_desc": "ABAP Cloud & RAP Developer · SAP S/4HANA Public Cloud Edition · "
                       "SAP BTP Side-by-Side · AI for ERP (MCP)",
        "kicker": "// SAP DEVELOPER — CALDAS NOVAS · GOIÁS · BRAZIL",
        "headline": "ABAP Cloud & RAP Developer  ·  SAP S/4HANA Public Cloud Edition",
        "subline": "SAP BTP Side-by-Side  ·  AI for ERP (MCP)",
        "sheet": "REV 2026 · SHEET 01",
        "arch_title": "How I build: SAP S/4HANA Clean Core with side-by-side extensions",
        "arch_desc": "SAP S/4HANA Public Cloud Edition in the center (ABAP Cloud, RAP, CDS Views; EWM and MM), "
                     "wrapped by an integration layer (OData, Communication Arrangements, SAP BTP, Integration "
                     "Suite), connected to side-by-side apps: Kotlin/Android warehouse apps on EWM, "
                     "Python/Streamlit automation, Java services, Fiori Elements and web UIs, Salesforce CRM "
                     "and AI agents via MCP.",
        "arch_kicker": "HOW I BUILD",
        "fig": "fig. 01 — clean core + side-by-side extensions",
        "integration": "INTEGRATION LAYER",
        "on_btp": "SIDE-BY-SIDE ON SAP BTP",
        "domains": "FUNCTIONAL DOMAINS",
        "released": "released APIs · upgrade-safe extensions",
        "left": [
            ("KOTLIN · ANDROID", "Warehouse apps", "RF data collection on SAP EWM"),
            ("PYTHON · STREAMLIT", "Internal automation", "Finance & HR routines"),
            ("JAVA", "Backend services", "Service layer next to the ERP"),
        ],
        "right": [
            ("FIORI ELEMENTS · WEB", "User interfaces", "Angular · React · TypeScript"),
            ("SALESFORCE", "CRM integration", "S/4HANA data exposed to the CRM"),
            ("AI · MCP", "LLM agents", "Natural-language access to the ERP"),
        ],
        # legend: labels plus the x of each marker (2nd..4th); text sits 40px / 14px after it
        "legend": ["data flow (OData / APIs)", "integration boundary",
                   "on-stack (Clean Core)", "communication scenario"],
        "legend_x": (250, 440, 650),
    },
    "pt-BR": {
        "banner_title": "João Victor R. V. Godoi — Desenvolvedor SAP",
        "banner_desc": "Desenvolvedor ABAP Cloud & RAP · SAP S/4HANA Public Cloud Edition · "
                       "SAP BTP Side-by-Side · IA para ERP (MCP)",
        "kicker": "// DESENVOLVEDOR SAP — CALDAS NOVAS · GOIÁS · BRASIL",
        "headline": "Desenvolvedor ABAP Cloud & RAP  ·  SAP S/4HANA Public Cloud Edition",
        "subline": "SAP BTP Side-by-Side  ·  IA para ERP (MCP)",
        "sheet": "REV 2026 · FOLHA 01",
        "arch_title": "Como eu construo: SAP S/4HANA Clean Core com extensões side-by-side",
        "arch_desc": "SAP S/4HANA Public Cloud Edition no centro (ABAP Cloud, RAP, CDS Views; EWM e MM), "
                     "envolvido por uma camada de integração (OData, Communication Arrangements, SAP BTP, "
                     "Integration Suite), conectado a apps side-by-side: apps de armazém em Kotlin/Android no EWM, "
                     "automação em Python/Streamlit, serviços Java, Fiori Elements e interfaces web, Salesforce CRM "
                     "e agentes de IA via MCP.",
        "arch_kicker": "COMO EU CONSTRUO",
        "fig": "fig. 01 — clean core + extensões side-by-side",
        "integration": "CAMADA DE INTEGRAÇÃO",
        "on_btp": "SIDE-BY-SIDE NO SAP BTP",
        "domains": "DOMÍNIOS FUNCIONAIS",
        "released": "APIs liberadas · extensões upgrade-safe",
        "left": [
            ("KOTLIN · ANDROID", "Apps de armazém", "Coleta de dados RF no SAP EWM"),
            ("PYTHON · STREAMLIT", "Automação interna", "Rotinas de finanças e RH"),
            ("JAVA", "Serviços de backend", "Camada de serviços ao lado do ERP"),
        ],
        "right": [
            ("FIORI ELEMENTS · WEB", "Interfaces de usuário", "Angular · React · TypeScript"),
            ("SALESFORCE", "Integração com CRM", "Dados do S/4HANA expostos ao CRM"),
            ("IA · MCP", "Agentes de LLM", "Acesso ao ERP em linguagem natural"),
        ],
        "legend": ["fluxo de dados (OData / APIs)", "fronteira de integração",
                   "on-stack (Clean Core)", "cenário de comunicação"],
        "legend_x": (290, 490, 690),
    },
}


def css_vars(p):
    return ";".join(f"--{k.replace('_', '-')}:{v}" for k, v in p.items())


def style_block(mode):
    """Class-based styles; colors come from CSS custom properties."""
    if mode == "auto":
        vars_css = (f":root{{{css_vars(PALETTES['light'])}}}"
                    f"@media (prefers-color-scheme: dark){{:root{{{css_vars(PALETTES['dark'])}}}}}")
    else:
        vars_css = f":root{{{css_vars(PALETTES[mode])}}}"
    return f"""<style>
{vars_css}
.bg{{fill:var(--bg)}} .panel{{fill:var(--panel)}}
.grid{{stroke:var(--grid);stroke-width:1}} .grid2{{stroke:var(--grid2);stroke-width:1}}
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
.t-text{{fill:var(--text)}} .t-muted{{fill:var(--muted)}} .t-accent{{fill:var(--accent)}}
.t-primary{{fill:var(--primary-text)}} .t-chip{{fill:var(--chip-text)}}
.wire{{fill:none;stroke:var(--line);stroke-width:1.6}}
.wire-flow{{fill:none;stroke:var(--accent);stroke-width:1.6;stroke-dasharray:4 14;opacity:.55;animation:flow 1.6s linear infinite}}
.node{{fill:var(--node);stroke:var(--node-stroke);stroke-width:1.2}}
.core{{fill:var(--core);stroke:var(--primary);stroke-width:1.6}}
.frame{{fill:none;stroke:var(--line);stroke-width:1.4;stroke-dasharray:6 6}}
.chip{{fill:var(--primary)}} .chip-o{{fill:none;stroke:var(--line);stroke-width:1.2}}
.chip-a{{fill:none;stroke:var(--accent);stroke-width:1.2}}
.bar{{fill:var(--primary)}} .bar-a{{fill:var(--accent)}}
.pulse{{fill:var(--accent)}} .halo{{fill:var(--accent);opacity:.22}}
.mark{{stroke:var(--accent);stroke-width:1.5;fill:none}}
.port{{fill:var(--bg);stroke:var(--accent);stroke-width:1.4}}
@keyframes flow{{to{{stroke-dashoffset:-36}}}}
@keyframes breathe{{0%,100%{{opacity:.35}}50%{{opacity:.9}}}}
.breathe{{animation:breathe 3.2s ease-in-out infinite}}
@media (prefers-reduced-motion: reduce){{.anim,.wire-flow,.breathe{{animation:none;display:none}}}}
</style>"""


def text(x, y, s, cls, size, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def chip_width(label, size, mono=False):
    per_char = size * (0.62 if mono else 0.56)
    return round(len(label) * per_char + size * 1.8)


def chip_row(cx, y, labels, size, h, kind="chip", gap=10, mono=False):
    """Centered row of rounded chips. kind: chip (filled) | chip-o | chip-a."""
    widths = [chip_width(l, size, mono) for l in labels]
    total = sum(widths) + gap * (len(labels) - 1)
    x = cx - total / 2
    out = []
    font = "mono" if mono else "sans"
    tcls = "t-chip" if kind == "chip" else ("t-accent" if kind == "chip-a" else "t-text")
    for label, w in zip(labels, widths):
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" class="{kind}"/>')
        out.append(text(f"{x + w / 2:.1f}", y + h / 2 + size * 0.36, label, f"{font} {tcls}", size, 600, "middle"))
        x += w + gap
    return "\n".join(out)


def pulse(path_id, dur, begin, reverse=False, r=3.2):
    kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if reverse else ""
    motion = (f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"{kp}>'
              f'<mpath xlink:href="#{path_id}"/></animateMotion>')
    return (f'<g class="anim"><circle r="{r * 2.4}" class="halo">{motion}</circle>'
            f'<circle r="{r}" class="pulse">{motion}</circle></g>')


def grid_defs(minor=20, major=100):
    return f"""<pattern id="g-minor" width="{minor}" height="{minor}" patternUnits="userSpaceOnUse">
  <path d="M{minor} 0H0V{minor}" fill="none" class="grid" opacity=".55"/></pattern>
<pattern id="g-major" width="{major}" height="{major}" patternUnits="userSpaceOnUse">
  <rect width="{major}" height="{major}" fill="url(#g-minor)"/>
  <path d="M{major} 0H0V{major}" fill="none" class="grid2" opacity=".7"/></pattern>"""


def corner_marks(w, h, inset=18, size=14):
    pts = [(inset, inset, 1, 1), (w - inset, inset, -1, 1), (inset, h - inset, 1, -1), (w - inset, h - inset, -1, -1)]
    return "\n".join(f'<path d="M{x} {y + sy * size}V{y}H{x + sx * size}" class="mark"/>' for x, y, sx, sy in pts)


def svg_open(w, h, title, desc, mode):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc">\n<title id="title">{escape(title)}</title>\n'
            f'<desc id="desc">{escape(desc)}</desc>\n{style_block(mode)}')


# --------------------------------------------------------------------------- banner

def banner(mode, lang="en"):
    W, H = 1200, 300
    t = STRINGS[lang]
    out = [svg_open(W, H, t["banner_title"], t["banner_desc"], mode)]
    out.append(f"<defs>{grid_defs()}"
               '<clipPath id="card"><rect width="1200" height="300" rx="16"/></clipPath></defs>')
    out.append('<g clip-path="url(#card)">')
    out.append(f'<rect width="{W}" height="{H}" class="bg"/>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#g-major)"/>')
    out.append(corner_marks(W, H))

    # left: identity
    out.append(text(64, 78, t["kicker"], "mono t-accent", 14, 500,
                    extra=' letter-spacing="1.2"'))
    out.append(text(62, 140, "João Victor R. V. Godoi", "sans t-text", 50, 700, extra=' letter-spacing="-0.5"'))
    out.append(f'<rect x="64" y="158" width="56" height="4" rx="2" class="bar"/>'
               f'<rect x="124" y="158" width="14" height="4" rx="2" class="bar-a"/>')
    out.append(text(64, 196, t["headline"], "sans t-text", 20, 500))
    out.append(text(64, 226, t["subline"], "sans t-muted", 20, 500))

    labels = ["ABAP Cloud", "RAP", "CDS", "OData", "BTP", "MCP"]
    x = 64
    for l in labels:
        w = chip_width(l, 12, mono=True)
        out.append(f'<rect x="{x}" y="248" width="{w}" height="24" rx="5" class="chip-o"/>')
        out.append(text(x + w / 2, 264, l, "mono t-primary", 12, 600, "middle"))
        x += w + 8

    # right: hub-and-spoke blueprint (core + side-by-side satellites)
    cx, cy = 968, 148
    sats = [(label, cx + dx, cy + dy) for label, dx, dy in (
        ("Kotlin", 0, -104), ("Python", 118, -56), ("Java", 118, 56),
        ("CRM", 0, 104), ("Fiori", -118, 56), ("MCP", -118, -56))]
    out.append(f'<circle cx="{cx}" cy="{cy}" r="112" class="frame"/>')
    for i, (label, sx, sy) in enumerate(sats):
        pid = f"b{i}"
        out.append(f'<path id="{pid}" d="M{cx} {cy}L{sx} {sy}" class="wire"/>')
        out.append(pulse(pid, 2.6, round(i * 0.43, 2), reverse=(i % 2 == 1), r=2.6))
    for label, sx, sy in sats:
        out.append(f'<circle cx="{sx}" cy="{sy}" r="20" class="node"/>')
        out.append(text(sx, sy + 4, label, "mono t-text", 10, 600, "middle"))
    out.append(f'<circle cx="{cx}" cy="{cy}" r="46" class="halo breathe"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="38" class="core"/>')
    out.append(text(cx, cy - 3, "S/4HANA", "sans t-text", 13, 700, "middle"))
    out.append(text(cx, cy + 13, "CLEAN CORE", "mono t-accent", 8.5, 600, "middle", ' letter-spacing="1"'))

    out.append(text(W - 40, H - 30, t["sheet"], "mono t-muted", 10, 500, "end", ' letter-spacing="1.5"'))
    out.append("</g></svg>")
    return "\n".join(out)


# ------------------------------------------------------------------- architecture

def node(x, y, w, h, tag, title, sub, accent_right=False):
    bar_x = x + w - 4 if accent_right else x
    tx = x + 20
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="node"/>',
        f'<rect x="{bar_x}" y="{y + 18}" width="4" height="{h - 36}" rx="2" class="bar-a"/>',
        text(tx, y + 28, tag, "mono t-accent", 11, 600, extra=' letter-spacing="1"'),
        text(tx, y + 54, title, "sans t-text", 18, 700),
        text(tx, y + 76, sub, "sans t-muted", 13, 400),
    ])


def architecture(mode, lang="en"):
    W, H = 1200, 660
    t = STRINGS[lang]
    out = [svg_open(W, H, t["arch_title"], t["arch_desc"], mode)]
    out.append(f"<defs>{grid_defs()}"
               f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>')
    out.append('<g clip-path="url(#card)">')
    out.append(f'<rect width="{W}" height="{H}" class="bg"/>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#g-major)"/>')
    out.append(corner_marks(W, H))

    out.append(text(40, 52, t["arch_kicker"], "mono t-accent", 13, 700, extra=' letter-spacing="2"'))
    out.append(text(W - 40, 52, t["fig"], "mono t-muted", 12, 500, "end"))

    # integration frame
    fx, fy, fw, fh = 365, 84, 470, 516
    out.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" class="panel" opacity=".55"/>')
    out.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" class="frame"/>')
    out.append(text(600, fy + 30, t["integration"], "mono t-accent", 11, 700, "middle", ' letter-spacing="2"'))
    out.append(chip_row(600, fy + 44, ["OData", "Communication Arrangements"], 13, 30, "chip-a"))
    out.append(chip_row(600, fy + fh - 74, ["SAP BTP", "Integration Suite"], 13, 30, "chip-a"))
    out.append(text(600, fy + fh - 18, t["on_btp"], "mono t-muted", 10, 600, "middle",
                    ' letter-spacing="2"'))

    # core
    cx0, cy0, cw, chh = 420, 180, 360, 316
    out.append(f'<rect x="{cx0 - 6}" y="{cy0 - 6}" width="{cw + 12}" height="{chh + 12}" rx="20" class="halo breathe"/>')
    out.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{chh}" rx="16" class="core"/>')
    out.append(text(600, cy0 + 34, "CLEAN CORE · ON-STACK", "mono t-accent", 11, 700, "middle", ' letter-spacing="2"'))
    out.append(text(600, cy0 + 72, "SAP S/4HANA", "sans t-text", 28, 800, "middle"))
    out.append(text(600, cy0 + 98, "Public Cloud Edition", "sans t-muted", 15, 500, "middle"))
    out.append(chip_row(600, cy0 + 120, ["ABAP Cloud", "RAP", "CDS Views"], 14, 34, "chip"))
    out.append(f'<path d="M{cx0 + 30} {cy0 + 180}H{cx0 + cw - 30}" class="grid2"/>')
    out.append(text(600, cy0 + 206, t["domains"], "mono t-muted", 10, 600, "middle", ' letter-spacing="2"'))
    out.append(chip_row(600, cy0 + 218, ["EWM", "MM"], 13, 28, "chip-o"))
    out.append(text(600, cy0 + 282, t["released"], "mono t-muted", 11, 500, "middle"))

    # side-by-side nodes + wires
    nw, nh = 270, 96
    ys = [130, 282, 434]
    ports = [cy0 + 70, cy0 + 158, cy0 + 246]
    wires, pulses, nodes, marks = [], [], [], []
    for i, (y, py) in enumerate(zip(ys, ports)):
        ncy = y + nh / 2
        for side, items in (("l", t["left"]), ("r", t["right"])):
            tag, title, sub = items[i]
            if side == "l":
                x, x0, c, x1 = 40, 40 + nw, fx, cx0
                nodes.append(node(x, y, nw, nh, tag, title, sub))
            else:
                x, x0, c, x1 = W - 40 - nw, W - 40 - nw, fx + fw, cx0 + cw
                nodes.append(node(x, y, nw, nh, tag, title, sub, accent_right=True))
            pid = f"w{side}{i}"
            d = f"M{x0} {ncy}C{c} {ncy} {c} {py} {x1} {py}"
            wires.append(f'<path id="{pid}" d="{d}" class="wire"/>')
            wires.append(f'<path d="{d}" class="wire-flow"/>')
            k = i * 2 + (side == "r")
            pulses.append(pulse(pid, 2.4, round(k * 0.37, 2), reverse=(k % 2 == 1)))
            marks.append(f'<rect x="{c - 5}" y="{(ncy + py) / 2 - 5}" width="10" height="10" '
                         f'transform="rotate(45 {c} {(ncy + py) / 2})" class="port"/>')
            marks.append(f'<circle cx="{x1}" cy="{py}" r="4" class="port"/>')
    out += wires + nodes + marks + pulses

    # legend
    ly = H - 26
    out.append(f'<path d="M40 {ly - 4}H72" class="wire"/>{pulse_static(56, ly - 4)}')
    l1, l2, l3, l4 = t["legend"]
    bx, cx, px = t["legend_x"]
    out.append(text(82, ly, l1, "sans t-muted", 12))
    out.append(f'<rect x="{bx}" y="{ly - 13}" width="30" height="18" rx="5" class="frame"/>')
    out.append(text(bx + 40, ly, l2, "sans t-muted", 12))
    out.append(f'<rect x="{cx}" y="{ly - 13}" width="30" height="18" rx="5" class="chip"/>')
    out.append(text(cx + 40, ly, l3, "sans t-muted", 12))
    out.append(f'<rect x="{px - 5}" y="{ly - 9}" width="10" height="10" transform="rotate(45 {px} {ly - 4})" class="port"/>')
    out.append(text(px + 14, ly, l4, "sans t-muted", 12))
    out.append("</g></svg>")
    return "\n".join(out)


def pulse_static(x, y):
    return f'<circle cx="{x}" cy="{y}" r="7" class="halo"/><circle cx="{x}" cy="{y}" r="3" class="pulse"/>'


# ------------------------------------------------------------------------ divider

def divider(mode):
    W, H = 1200, 28
    out = [svg_open(W, H, "section divider", "thin divider", mode)]
    out.append('<defs><linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">'
               '<stop offset="0" style="stop-color:var(--line);stop-opacity:0"/>'
               '<stop offset=".5" style="stop-color:var(--line);stop-opacity:1"/>'
               '<stop offset="1" style="stop-color:var(--line);stop-opacity:0"/></linearGradient></defs>')
    out.append(f'<rect x="0" y="13.5" width="{W}" height="1" fill="url(#fade)"/>')
    out.append('<rect x="594" y="8" width="12" height="12" transform="rotate(45 600 14)" class="port"/>')
    out.append('<circle cx="600" cy="14" r="2.2" class="pulse"/>')
    out.append('<circle cx="560" cy="14" r="1.8" class="pulse" opacity=".6"/>'
               '<circle cx="640" cy="14" r="1.8" class="pulse" opacity=".6"/>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    ASSETS.mkdir(exist_ok=True)
    for mode in ("dark", "light"):
        (ASSETS / f"divider-{mode}.svg").write_text(divider(mode) + "\n", encoding="utf-8")
    for lang in STRINGS:
        suffix = "" if lang == "en" else f"-{lang}"
        for name, fn in (("banner", banner), ("architecture", architecture)):
            for mode in ("dark", "light"):
                (ASSETS / f"{name}{suffix}-{mode}.svg").write_text(fn(mode, lang) + "\n", encoding="utf-8")
        (ASSETS / f"architecture{suffix}.svg").write_text(architecture("auto", lang) + "\n", encoding="utf-8")
    print("wrote", sorted(p.name for p in ASSETS.glob("*.svg")))


if __name__ == "__main__":
    main()
