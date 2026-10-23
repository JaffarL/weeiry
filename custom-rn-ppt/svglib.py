"""极简 SVG 绘图库：生成可被 svg2pptx.py 还原为原生 PPT 形状的 SVG。

约定：只使用 rect / circle / polygon / polyline / text 五种元素；
文本元素在 data-pptx 中携带段落结构（JSON），以便转换为可编辑文本框。
"""
import html
import json
import re

W, H = 1280, 720
FONT = "'Microsoft YaHei','微软雅黑','PingFang SC','WenQuanYi Zen Hei',sans-serif"

# 中兴通讯品牌蓝 #0085CC 为主色，四个部分各配一个强调色
C = dict(
    brand='#0085CC', deep='#005B8F', navy='#0B3A5B', light='#E3F2FB', light2='#F2F8FC',
    text='#1F2D3D', sub='#4F5F6F', mute='#8A99A8', line='#D3E2EC',
    red='#D9483B', redl='#FCEDEB', orange='#E8892B', orangel='#FDF2E6',
    green='#1F9D6B', greenl='#E6F5EE', teal='#0FA3A3', teall='#E2F5F5',
    gray='#7B8794', grayl='#F1F3F5', beige='#FBF3E3', white='#FFFFFF',
)

_COLOR_ALIAS = {k: v for k, v in C.items()}
_MARK = re.compile(r'\{(b)?(#[0-9A-Fa-f]{6}|[a-z]+)?:(.*?)\}')


def parse_runs(s, color, bold):
    """'普通{red:红色}{b:粗体}{b#0085CC:蓝色粗体}' -> [(text, color, bold), ...]"""
    runs, pos = [], 0
    for m in _MARK.finditer(s):
        if m.start() > pos:
            runs.append((s[pos:m.start()], color, bold))
        c = m.group(2)
        c = _COLOR_ALIAS.get(c, c) if c else color
        runs.append((m.group(3), c, bold or bool(m.group(1))))
        pos = m.end()
    if pos < len(s):
        runs.append((s[pos:], color, bold))
    return [r for r in runs if r[0]]


def char_w(ch, size):
    o = ord(ch)
    if ch == ' ':
        return size * 0.3
    if o < 128:
        return size * (0.62 if ch.isupper() else 0.55)
    return size


_NO_START = set('，。、；：？！）》」』”’,.;:!?)%')


def wrap_runs(runs, width, size):
    """把 runs 按宽度折行，返回 [[(text,color,bold),...], ...]。"""
    tokens = []  # (text, color, bold)
    for text, color, bold in runs:
        for t in re.findall(r'[A-Za-z0-9.\-_/+]+|.', text):
            tokens.append((t, color, bold))
    lines, cur, cur_w = [], [], 0.0
    for t, color, bold in tokens:
        tw = sum(char_w(ch, size) for ch in t)
        if cur and cur_w + tw > width and t not in _NO_START and t != ' ':
            lines.append(cur)
            cur, cur_w = [], 0.0
        if not cur and t == ' ':
            continue
        cur.append((t, color, bold))
        cur_w += tw
    if cur:
        lines.append(cur)
    merged = []
    for line in lines:
        m = []
        for t, color, bold in line:
            if m and m[-1][1] == color and m[-1][2] == bold:
                m[-1] = (m[-1][0] + t, color, bold)
            else:
                m.append((t, color, bold))
        merged.append(m)
    return merged or [[('', C['text'], False)]]


def esc(s):
    return html.escape(s, quote=True)


class Slide:
    def __init__(self, bg=C['white']):
        self.els = []
        self.markers = set()
        self.rect(0, 0, W, H, fill=bg)

    # ---------- 基本形状 ----------
    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1, rx=0, dash=False, opacity=1):
        a = f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"'
        if rx:
            a += f' rx="{rx}"'
        self.els.append(f'<rect {a} {self._paint(fill, stroke, sw, dash, opacity)}/>')

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1, dash=False):
        self.els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {self._paint(fill, stroke, sw, dash)}/>')

    def poly(self, pts, fill=None, stroke=None, sw=1, dash=False):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        self.els.append(f'<polygon points="{p}" {self._paint(fill, stroke, sw, dash)}/>')

    def line(self, pts, color=C['gray'], sw=2, arrow=True, dash=False, start_arrow=False):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        a = f'points="{p}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"'
        if dash:
            a += ' stroke-dasharray="6,4"'
        mid = 'arr' + color.lstrip('#')
        if arrow:
            self.markers.add(color)
            a += f' marker-end="url(#{mid})"'
        if start_arrow:
            self.markers.add(color)
            a += f' marker-start="url(#{mid}s)"'
        self.els.append(f'<polyline {a}/>')

    def _paint(self, fill, stroke, sw, dash, opacity=1):
        a = f'fill="{fill or "none"}"'
        if opacity != 1:
            a += f' fill-opacity="{opacity}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
            if dash:
                a += ' stroke-dasharray="6,4"'
        return a

    # ---------- 文本 ----------
    def text(self, x, y, w, h, paras, size=16, color=C['text'], bold=False, align='l',
             valign='t', lh=1.4, gap=0, bullet=None, bullet_color=None):
        if isinstance(paras, str):
            paras = paras.split('\n')
        indent = size * 1.1 if bullet else 0
        bullet_color = bullet_color or color
        model, wrapped = [], []
        for p in paras:
            runs = parse_runs(p, color, bold)
            model.append([list(r) for r in runs])
            wrapped.append(wrap_runs(runs, w - indent, size))
        n_lines = sum(len(x) for x in wrapped)
        block = n_lines * size * lh + gap * (len(paras) - 1)
        top = y if valign == 't' else (y + (h - block) / 2 if valign == 'm' else y + h - block)
        anchor = {'l': 'start', 'c': 'middle', 'r': 'end'}[align]
        ax = {'l': x, 'c': x + w / 2, 'r': x + w}[align]
        tsp = []
        cy = top
        for lines in wrapped:
            for i, line in enumerate(lines):
                base = cy + size * lh / 2 + size * 0.36
                lx = ax + (indent if align == 'l' else 0)
                if bullet and i == 0:
                    tsp.append(f'<tspan x="{x:.1f}" y="{base:.1f}" fill="{bullet_color}" text-anchor="start">{esc(bullet)}</tspan>')
                fw = ' font-weight="700"'
                inner = ''.join(
                    f'<tspan fill="{c}"{fw if b else ""}>{esc(t)}</tspan>'
                    for t, c, b in line)
                tsp.append(f'<tspan x="{lx:.1f}" y="{base:.1f}">{inner}</tspan>')
                cy += size * lh
            cy += gap
        meta = dict(box=[x, y, w, h], size=size, align=align, valign=valign, lh=lh, gap=gap,
                    bullet=bullet, bullet_color=bullet_color, paras=model)
        self.els.append(
            f'<text font-size="{size}" text-anchor="{anchor}" font-family="{esc(FONT)}" '
            f"data-pptx='{esc(json.dumps(meta, ensure_ascii=False))}'>{''.join(tsp)}</text>")

    # ---------- 组合图形 ----------
    def box(self, x, y, w, h, txt, fill=C['light'], stroke=None, color=C['text'], size=15,
            bold=False, rx=6, align='c', sw=1.2, pad=10, valign='m', **kw):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=rx, sw=sw)
        self.text(x + pad, y + 4, w - 2 * pad, h - 8, txt, size=size, color=color, bold=bold,
                  align=align, valign=valign, **kw)

    def diamond(self, cx, cy, w, h, txt, fill=C['beige'], stroke=C['orange'], size=13, color=C['text']):
        self.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
                  fill=fill, stroke=stroke, sw=1.2)
        self.text(cx - w / 2 + 18, cy - h / 2 + 4, w - 36, h - 8, txt, size=size, color=color,
                  align='c', valign='m', lh=1.25)

    def chevron(self, x, y, w, h, fill, notch=18, first=False):
        pts = [(x, y), (x + w - notch, y), (x + w, y + h / 2), (x + w - notch, y + h), (x, y + h)]
        if not first:
            pts.append((x + notch, y + h / 2))
        self.poly(pts, fill=fill)

    def check(self, cx, cy, r=11, color=C['green']):
        self.circle(cx, cy, r, fill=color)
        self.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)],
                  color=C['white'], sw=max(2, r / 5), arrow=False)

    def cross(self, cx, cy, r=11, color=C['red']):
        self.circle(cx, cy, r, fill=color)
        d = r * 0.38
        self.line([(cx - d, cy - d), (cx + d, cy + d)], color=C['white'], sw=max(2, r / 5), arrow=False)
        self.line([(cx - d, cy + d), (cx + d, cy - d)], color=C['white'], sw=max(2, r / 5), arrow=False)

    def person(self, cx, cy, color=C['brand'], s=1.0):
        self.circle(cx, cy - 9 * s, 7 * s, fill=color)
        self.rect(cx - 11 * s, cy + 1 * s, 22 * s, 13 * s, fill=color, rx=6 * s)

    def num(self, cx, cy, n, color, r=14, size=15):
        self.circle(cx, cy, r, fill=color)
        self.text(cx - r, cy - r, 2 * r, 2 * r, str(n), size=size, color=C['white'], bold=True,
                  align='c', valign='m', lh=1.0)

    # ---------- 输出 ----------
    def svg(self):
        defs = []
        for c in sorted(self.markers):
            mid = 'arr' + c.lstrip('#')
            defs.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
                        f'markerHeight="5" orient="auto"><polygon points="0,0 10,5 0,10" fill="{c}"/></marker>')
            defs.append(f'<marker id="{mid}s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="5" '
                        f'markerHeight="5" orient="auto-start-reverse"><polygon points="0,0 10,5 0,10" fill="{c}"/></marker>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
                f'font-family="{esc(FONT)}">\n<defs>{"".join(defs)}</defs>\n' + '\n'.join(self.els) + '\n</svg>\n')
