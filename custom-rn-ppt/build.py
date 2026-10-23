"""构建流程：slides.py → svg/*.svg → index.html（预览）→ 国际定制RN流程改进.pptx（可编辑）。"""
from pathlib import Path

import svg2pptx
from slides import SLIDES

HERE = Path(__file__).parent
SVG_DIR = HERE / 'svg'
PPTX = HERE / '国际定制RN流程改进.pptx'


def main():
    SVG_DIR.mkdir(exist_ok=True)
    files, inline = [], []
    for i, fn in enumerate(SLIDES, 1):
        svg = fn().svg()
        f = SVG_DIR / f'slide-{i:02d}.svg'
        f.write_text(svg, encoding='utf-8')
        files.append(f)
        inline.append(f'<section class="slide" id="s{i}">{svg}</section>')
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>国际定制RN流程改进</title>
<style>
  body {{ margin: 0; background: #E9EEF2; font-family: 'Microsoft YaHei', sans-serif; }}
  .wrap {{ max-width: 1280px; margin: 24px auto; padding: 0 16px; }}
  .slide {{ margin: 0 0 24px; box-shadow: 0 2px 12px rgba(0,0,0,.12); background: #fff; line-height: 0; }}
  .slide svg {{ width: 100%; height: auto; display: block; }}
</style></head>
<body><div class="wrap">
{chr(10).join(inline)}
</div></body></html>
'''
    (HERE / 'index.html').write_text(html, encoding='utf-8')
    svg2pptx.build(files, PPTX)
    print(f'{len(files)} slides: svg/ + index.html + {PPTX.name}')


if __name__ == '__main__':
    main()
