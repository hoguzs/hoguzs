"""Çöp adamın odasını (assets/oda.svg) üretir: gerçek tarih, gece/gündüz ve günün aktivitesi."""
import calendar
import random

T = 12.0
W, H = 900, 260
MONO = "font-family=\"'SF Mono',Menlo,Consolas,'Liberation Mono','Courier New',monospace\""
G = "#8b949e"
MONTHS = ["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN", "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"]
VARIANTS = ["typing", "reading", "coffee", "thinking", "dancing"]


def anim(attr, pts, discrete=False):
    kt = ";".join(f"{t / T:.4f}" for t, _ in pts)
    vs = ";".join(str(v) for _, v in pts)
    mode = ' calcMode="discrete"' if discrete else ""
    return f'<animate attributeName="{attr}" values="{vs}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"{mode}/>'


def clip(cid, x, y, h, w, t0, t1):
    return f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}">{anim("width", [(0, 0), (t0, 0), (t1, w), (T, w)])}</rect></clipPath>'


def phase_a():
    return anim("opacity", [(0, 1), (6.6, 0), (11.6, 1)], True)


def books_svg():
    rnd = random.Random(5)
    out = []
    for b in [102, 144, 186, 228]:
        x = 23
        while x < 84:
            w = rnd.choice([5, 6, 7, 8, 9])
            h = rnd.choice([22, 26, 30, 34, 37])
            if x + w > 88:
                break
            lean = rnd.random() < 0.07
            tr = f' transform="rotate(8 {x} {b})"' if lean else ""
            out.append(f'<rect x="{x}" y="{b - h}" width="{w}" height="{h}" rx="1" fill="#161b22" stroke="{G}" stroke-width="1.3"{tr}/>')
            if rnd.random() < 0.6:
                out.append(f'<line x1="{x + 1.5}" y1="{b - h + 6}" x2="{x + w - 1.5}" y2="{b - h + 6}" stroke="{G}" stroke-width="1"/>')
            x += w + rnd.choice([1, 1, 2]) + (5 if lean else 0)
    return "\n".join(out)


def stars_svg():
    rnd = random.Random(3)
    return "\n".join(
        f'<circle cx="{rnd.randint(190, 218)}" cy="{rnd.randint(30, 66)}" r="{rnd.choice([0.8, 1, 1.3])}" fill="#fff"><animate attributeName="opacity" values="0.15;1;0.15" dur="{rnd.uniform(1.5, 4):.1f}s" begin="{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(7)
    )


def window(night):
    if night:
        sky = f'<rect x="186" y="28" width="38" height="48" fill="#0a0f1a"/>{stars_svg()}<circle cx="203" cy="44" r="8" fill="#e6edf3"/><circle cx="207" cy="41" r="7" fill="#0a0f1a"/>'
    else:
        sky = ('<rect x="186" y="28" width="38" height="48" fill="#1f3447"/><circle cx="212" cy="42" r="7" fill="#e3b341"/>'
               '<g fill="#c9d1d9" opacity="0.85"><ellipse cx="198" cy="60" rx="9" ry="3.5"/><ellipse cx="204" cy="57" rx="6" ry="3.5"/>'
               '<animateTransform attributeName="transform" type="translate" values="-3 0;3 0;-3 0" dur="12s" repeatCount="indefinite"/></g>')
    return f'''<g>
 {sky}
 <rect x="184" y="26" width="42" height="52" rx="2" fill="none" stroke="#c9d1d9" stroke-width="2.2"/>
 <line x1="205" y1="26" x2="205" y2="78" stroke="#c9d1d9" stroke-width="1.6"/>
 <line x1="184" y1="52" x2="226" y2="52" stroke="#c9d1d9" stroke-width="1.6"/>
 <line x1="181" y1="80" x2="229" y2="80" stroke="#c9d1d9" stroke-width="2.4" stroke-linecap="round"/>
</g>'''


def calendar_svg(today):
    weeks = calendar.Calendar(0).monthdayscalendar(today.year, today.month)
    cells, tick = [], ""
    for r, week in enumerate(weeks):
        for c, d in enumerate(week):
            if not d:
                continue
            x, y = 259 + c * 9.2, 111 + r * 7.2
            fill = "#484f58" if d < today.day else "#30363d"
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="5.2" height="4.6" rx="1" fill="{fill}"/>')
            if d == today.day:
                cells.append(f'<rect x="{x - 1.4:.1f}" y="{y - 1.4:.1f}" width="8" height="7.4" rx="2" fill="none" stroke="#3fb950" stroke-width="1.4"/>')
                tick = (f'<path d="M{x - 0.2:.1f} {y + 2.4:.1f} l2.3 2.3 l4.4 -5.4" fill="none" stroke="#3fb950" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="14" stroke-dashoffset="0">'
                        f'<animate attributeName="stroke-dashoffset" values="14;14;0;0;14" keyTimes="0;0.5083;0.5417;0.9583;1" dur="12s" repeatCount="indefinite"/></path>')
    label = f"{today.day} {MONTHS[today.month - 1]}"
    return f'''<g>
 <line x1="289" y1="86" x2="289" y2="92" stroke="{G}" stroke-width="1.5"/>
 <rect x="253" y="92" width="72" height="66" rx="4" fill="#161b22" stroke="#c9d1d9" stroke-width="2"/>
 <path d="M253 96 a4 4 0 0 1 4 -4 h64 a4 4 0 0 1 4 4 v10 h-72 z" fill="#30363d" stroke="#c9d1d9" stroke-width="2" stroke-linejoin="round"/>
 <text x="289" y="103" text-anchor="middle" {MONO} font-size="8" fill="#c9d1d9" letter-spacing="1.2">{label}</text>
 {"".join(cells)}
 {tick}
</g>'''


def lamp(night):
    cone = ('<polygon points="152,38 168,38 222,204 98,204" fill="#fff" opacity="0.045"><animate attributeName="opacity" values="0.03;0.06;0.03" dur="5s" repeatCount="indefinite"/></polygon>'
            '<circle cx="160" cy="41" r="6" fill="#e3b341" opacity="0.25"/>') if night else ""
    bulb = "#f6e7a8" if night else "#484f58"
    return f'''<g>
 {cone}
 <line x1="160" y1="0" x2="160" y2="22" stroke="{G}" stroke-width="2"/>
 <path d="M148 38 L154 22 H166 L172 38 Z" fill="#161b22" stroke="#c9d1d9" stroke-width="2" stroke-linejoin="round"/>
 <circle cx="160" cy="41" r="2.6" fill="{bulb}"/>
</g>'''


def activity(variant):
    """(kollar, baş eki) — 0-6.6 sn arası gösterilen etkinlik."""
    rest_l = '<polyline points="138,118 130,150 148,166"/>'
    if variant == "reading":
        arms = ('<polyline points="138,118 134,138 144,143"/><polyline points="182,118 186,138 176,143"/>'
                f'<path d="M138 128 l22 -5 l22 5 v21 l-22 -4 l-22 4 z" fill="#161b22"/><line x1="160" y1="123" x2="160" y2="145"/>'
                '<path d="M162 124 q9 -7 17 1" stroke-width="1.6"><animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/></path>')
        return arms, ""
    if variant == "coffee":
        arms = (rest_l +
                '<g><animateTransform attributeName="transform" type="rotate" values="0 182 118;-6 182 118;0 182 118" dur="3s" repeatCount="indefinite"/>'
                '<polyline points="182,118 200,114 191,98"/>'
                '<rect x="190" y="84" width="12" height="14" rx="2" fill="#161b22"/><path d="M202 88 h3 a3 3 0 0 1 0 7 h-3"/>'
                '<path d="M194 80 q-3 -4 0 -8" stroke="#8b949e" stroke-width="1.6"><animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/></path></g>')
        return arms, ""
    if variant == "thinking":
        arms = (rest_l + '<polyline points="182,118 196,132 173,108"/>')
        extra = (f'<text x="196" y="78" {MONO} font-size="18" font-weight="700" fill="#c9d1d9" stroke="none">?'
                 '<animate attributeName="opacity" values="0;1;1;0" dur="2.4s" repeatCount="indefinite"/></text>')
        return arms, extra
    if variant == "dancing":
        arms = ('<g><animateTransform attributeName="transform" type="rotate" values="25 138 118;-25 138 118;25 138 118" dur="0.8s" repeatCount="indefinite"/>'
                '<line x1="138" y1="118" x2="124" y2="82"/><circle cx="123.5" cy="79" r="3" fill="#c9d1d9" stroke="none"/></g>'
                '<g><animateTransform attributeName="transform" type="rotate" values="-25 182 118;25 182 118;-25 182 118" dur="0.8s" repeatCount="indefinite"/>'
                '<line x1="182" y1="118" x2="196" y2="82"/><circle cx="196.5" cy="79" r="3" fill="#c9d1d9" stroke="none"/></g>')
        extra = ('<path d="M142 88 a18 18 0 0 1 36 0" fill="none"/><rect x="139" y="85" width="5" height="10" rx="2" fill="#c9d1d9" stroke="none"/><rect x="176" y="85" width="5" height="10" rx="2" fill="#c9d1d9" stroke="none"/>'
                 f'<text x="206" y="66" {MONO} font-size="16" fill="#3fb950" stroke="none">♪<animate attributeName="opacity" values="0;1;0" dur="1.6s" repeatCount="indefinite"/><animate attributeName="y" values="74;56" dur="1.6s" repeatCount="indefinite"/></text>'
                 f'<text x="112" y="70" {MONO} font-size="14" fill="#3fb950" stroke="none">♫<animate attributeName="opacity" values="0;1;0" dur="1.6s" begin="0.8s" repeatCount="indefinite"/><animate attributeName="y" values="78;60" dur="1.6s" begin="0.8s" repeatCount="indefinite"/></text>')
        return arms, extra
    arms = ('<polyline points="138,118 130,150 148,166"><animateTransform attributeName="transform" type="translate" values="0 0;0 3;0 0" dur="0.32s" repeatCount="indefinite"/></polyline>'
            '<polyline points="182,118 190,150 172,166"><animateTransform attributeName="transform" type="translate" values="0 3;0 0;0 3" dur="0.32s" repeatCount="indefinite"/></polyline>')
    return arms, ""


def build(today, night, variant):
    arms, head_extra = activity(variant)
    shelf_books = books_svg()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Selam, ben Oğuz">
<defs>
{clip("c1", 382, 64, 16, 120, 0.5, 1.4)}
{clip("c3", 382, 114, 16, 200, 2.6, 3.8)}
{clip("c5", 380, 182, 40, 330, 6.8, 8.8)}
<clipPath id="r"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="#0d1117"/>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="#30363d" stroke-width="1.5"/>
<rect x="0" y="228" width="900" height="32" fill="#0a0d12"/>
<line x1="0" y1="228" x2="900" y2="228" stroke="#30363d" stroke-width="2"/>
{lamp(night)}
{window(night)}
<g>
 <rect x="18" y="60" width="74" height="168" fill="#11161d" stroke="#c9d1d9" stroke-width="2.5"/>
 <line x1="18" y1="102" x2="92" y2="102" stroke="#c9d1d9" stroke-width="2"/>
 <line x1="18" y1="144" x2="92" y2="144" stroke="#c9d1d9" stroke-width="2"/>
 <line x1="18" y1="186" x2="92" y2="186" stroke="#c9d1d9" stroke-width="2"/>
 {shelf_books}
 <path d="M44 60 l2 -10 h14 l2 10" fill="#161b22" stroke="#c9d1d9" stroke-width="2" stroke-linejoin="round"/>
 <g stroke="#3fb950" stroke-width="2" stroke-linecap="round" fill="none"><g><path d="M53 50 q-8 -8 -6 -18"/><path d="M53 50 q0 -12 2 -22"/><path d="M53 50 q9 -6 9 -16"/>
 <animateTransform attributeName="transform" type="rotate" values="-1.5 53 50;1.5 53 50;-1.5 53 50" dur="4s" repeatCount="indefinite"/></g></g>
</g>
<g>
 <line x1="117" y1="60" x2="117" y2="66" stroke="{G}" stroke-width="1.5"/>
 <rect x="100" y="66" width="34" height="42" rx="2" fill="#161b22" stroke="#c9d1d9" stroke-width="2"/>
 <text x="117" y="92" text-anchor="middle" {MONO} font-size="14" font-weight="700" fill="#3fb950">&lt;/&gt;</text>
 <line x1="107" y1="99" x2="127" y2="99" stroke="{G}" stroke-width="1.5"/>
</g>
{calendar_svg(today)}
<g stroke="#c9d1d9" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="#11161d">
 <ellipse cx="222" cy="219" rx="25" ry="9"><animate attributeName="ry" values="9;10;9" dur="3s" repeatCount="indefinite"/><animate attributeName="cy" values="219;218;219" dur="3s" repeatCount="indefinite"/></ellipse>
 <path d="M246 221 q12 -2 10 -10 q-1 -4 -6 -3" fill="none"/>
 <circle cx="198" cy="218" r="8"/>
 <path d="M192 212 l-1 -7 l6 4 M200 210 l3 -7 l2 8" fill="none"/>
 <path d="M194 219 h3 M200 219 h3" fill="none" stroke-width="1.6"/>
</g>
<g {MONO} font-size="11" fill="{G}">
 <text x="206" y="204">z<animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/><animate attributeName="y" values="206;196" dur="3s" repeatCount="indefinite"/></text>
 <text x="214" y="204">Z<animate attributeName="opacity" values="0;1;0" dur="3s" begin="1s" repeatCount="indefinite"/><animate attributeName="y" values="206;192" dur="3s" begin="1s" repeatCount="indefinite"/></text>
</g>
<line x1="100" y1="204" x2="340" y2="204" stroke="#c9d1d9" stroke-width="3" stroke-linecap="round"/>
<line x1="116" y1="206" x2="116" y2="228" stroke="{G}" stroke-width="3" stroke-linecap="round"/>
<line x1="324" y1="206" x2="324" y2="228" stroke="{G}" stroke-width="3" stroke-linecap="round"/>

<g stroke="#c9d1d9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
 <g>
  <circle cx="160" cy="88" r="17" fill="#0d1117"/>
  <circle cx="153.5" cy="85" r="1.8" fill="#c9d1d9" stroke="none"/>
  <circle cx="166.5" cy="85" r="1.8" fill="#c9d1d9" stroke="none"/>
  <path d="M153 94 Q160 94 167 94"><animate attributeName="d" values="M153 94 Q160 94 167 94;M153 94 Q160 94 167 94;M153 93 Q160 102 167 93;M153 93 Q160 102 167 93;M153 94 Q160 94 167 94" keyTimes="0;0.5;0.55;0.96;1" dur="12s" repeatCount="indefinite"/></path>
  <g opacity="1">{phase_a()}{head_extra}</g>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 2;0 0" dur="0.6s" repeatCount="indefinite"/>
 </g>
 <line x1="160" y1="105" x2="160" y2="152"/>
 <line x1="138" y1="118" x2="182" y2="118"/>
 <g opacity="0">{phase_a()}{arms}</g>
 <g>
  {anim("opacity", [(0, 0), (6.6, 1), (11.6, 0)], True)}
  <polyline points="138,118 130,150 148,166"/>
  <polyline points="182,118 208,100"/>
  <g>
   <animateTransform attributeName="transform" type="rotate" values="-22 208 100;22 208 100;-22 208 100" dur="0.55s" repeatCount="indefinite"/>
   <line x1="208" y1="100" x2="214" y2="70"/>
   <circle cx="215" cy="66" r="3.5" fill="#c9d1d9" stroke="none"/>
  </g>
 </g>
</g>

<rect x="104" y="152" width="112" height="52" rx="5" fill="#161b22" stroke="#c9d1d9" stroke-width="2.5"/>
<circle cx="160" cy="178" r="6" fill="none" stroke="{G}" stroke-width="2"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></circle>
<line x1="88" y1="204" x2="232" y2="204" stroke="#c9d1d9" stroke-width="3" stroke-linecap="round"/>

<g stroke="#c9d1d9" stroke-width="2.5" fill="none" stroke-linecap="round">
 <path d="M272 184 h20 v14 a6 6 0 0 1 -6 6 h-8 a6 6 0 0 1 -6 -6 z" fill="#161b22"/>
 <path d="M292 188 h4 a4 4 0 0 1 0 9 h-4"/>
 <g stroke="{G}" stroke-width="2">
  <path d="M278 176 q-4 -6 0 -12"><animate attributeName="opacity" values="0;0.9;0" dur="2.4s" repeatCount="indefinite"/></path>
  <path d="M286 176 q4 -6 0 -12"><animate attributeName="opacity" values="0;0.9;0" dur="2.4s" begin="1.2s" repeatCount="indefinite"/></path>
 </g>
</g>

<g opacity="0">
 {anim("opacity", [(0, 0), (7.0, 1), (10.8, 0)], True)}
 <path d="M236 44 h74 a8 8 0 0 1 8 8 v20 a8 8 0 0 1 -8 8 h-60 l-12 10 v-10 h-2 a8 8 0 0 1 -8 -8 v-20 a8 8 0 0 1 8 -8z" fill="#161b22" stroke="#c9d1d9" stroke-width="2"/>
 <text x="273" y="68" text-anchor="middle" {MONO} font-size="15" fill="#c9d1d9">selam!</text>
</g>

<g>
 {anim("opacity", [(0, 1), (11.3, 1), (11.8, 0), (12, 0)])}
 <rect x="360" y="24" width="520" height="212" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
 <line x1="360" y1="52" x2="880" y2="52" stroke="#30363d" stroke-width="1.5"/>
 <circle cx="380" cy="38" r="5" fill="#30363d"/><circle cx="398" cy="38" r="5" fill="#30363d"/><circle cx="416" cy="38" r="5" fill="#30363d"/>
 <text x="620" y="43" text-anchor="middle" {MONO} font-size="12" fill="{G}">oguz@dev: ~</text>
 <g clip-path="url(#c1)"><text x="382" y="76" {MONO} font-size="15"><tspan fill="#3fb950">$</tspan><tspan fill="#c9d1d9"> whoami</tspan></text></g>
 <text x="382" y="98" {MONO} font-size="15" fill="{G}" opacity="0">oguz{anim("opacity", [(0, 0), (1.8, 1), (12, 1)], True)}</text>
 <g clip-path="url(#c3)"><text x="382" y="126" {MONO} font-size="15"><tspan fill="#3fb950">$</tspan><tspan fill="#c9d1d9"> ./selam.sh</tspan></text></g>
 <g>
  {anim("opacity", [(0, 0), (3.9, 1), (12, 1)], True)}
  <text x="382" y="150" {MONO} font-size="15" fill="{G}">derleniyor</text>
  <rect x="492" y="138" width="150" height="12" rx="3" fill="none" stroke="{G}" stroke-width="1.2"/>
  <rect x="494" y="140" width="0" height="8" rx="2" fill="#c9d1d9">{anim("width", [(0, 0), (4.0, 0), (6.0, 146), (12, 146)])}</rect>
  <text x="654" y="150" {MONO} font-size="15" fill="#3fb950" opacity="0">✓ tamam{anim("opacity", [(0, 0), (6.1, 1), (12, 1)], True)}</text>
 </g>
 <g clip-path="url(#c5)"><text x="382" y="208" {MONO} font-size="30" font-weight="700"><tspan fill="#3fb950">&gt;</tspan><tspan fill="#f0f6fc"> Selam, ben Oğuz</tspan></text></g>
 <rect x="690" y="186" width="14" height="26" fill="#c9d1d9" opacity="0">{anim("opacity", [(0, 0), (8.8, 1), (9.3, 0), (9.8, 1), (10.3, 0), (10.8, 1), (12, 1)], True)}</rect>
</g>
</g>
</svg>'''
    return svg
