"""14 页幻灯片内容与版式定义。运行 build.py 生成 SVG / HTML / PPTX。"""
from svglib import Slide, C, W, H

TOTAL = 14
PARTS = {
    0: ('前言', C['gray'], C['grayl']),
    1: ('01 痛点问题', C['red'], C['redl']),
    2: ('02 原因分析', C['orange'], C['orangel']),
    3: ('03 解决方案', C['brand'], C['light']),
    4: ('04 成果收益', C['green'], C['greenl']),
}


def frame(no, part, title, subtitle=None):
    s = Slide()
    s.rect(60, 42, 6, 36, fill=C['brand'])
    s.text(80, 36, 960, 48, title, size=28, color=C['navy'], bold=True, valign='m', lh=1.2)
    if part is not None:
        name, c, cl = PARTS[part]
        s.rect(1080, 46, 140, 30, fill=cl, rx=15)
        s.text(1080, 46, 140, 30, name, size=14, color=c, bold=True, align='c', valign='m', lh=1.0)
    if subtitle:
        s.text(80, 86, 1140, 30, subtitle, size=15, color=C['sub'], valign='m', lh=1.3)
    s.line([(60, 688), (1220, 688)], color=C['line'], sw=1, arrow=False)
    s.text(60, 692, 600, 20, '国际定制RN流程改进 ｜ CCN文档团队', size=11, color=C['mute'], valign='m', lh=1.0)
    s.text(1020, 692, 200, 20, f'{no} / {TOTAL}', size=11, color=C['mute'], align='r', valign='m', lh=1.0)
    return s


# ------------------------------------------------------------------ 01 封面
def s01():
    s = Slide()
    s.rect(0, 0, 760, H, fill=C['brand'])
    s.rect(760, 0, 520, H, fill=C['light2'])
    s.text(80, 170, 600, 30, 'CCN文档团队 · 改进专项汇报', size=18, color='#CFE9F8', lh=1.2)
    s.text(80, 220, 640, 160, '国际定制RN\n流程改进', size=58, color=C['white'], bold=True, lh=1.25)
    s.rect(80, 405, 80, 5, fill=C['white'])
    s.text(80, 430, 640, 44, '搭车主业务，打通需求断链', size=30, color=C['white'], lh=1.2)
    s.text(80, 600, 400, 26, '2026年', size=16, color='#CFE9F8', lh=1.2)
    # 右侧：四个节点的链路示意
    s.text(830, 110, 380, 26, '定制RN需求的贯通之路', size=16, color=C['deep'], bold=True, lh=1.2)
    nodes = [('iDOP', '升级方案申请时勾选需求'), ('RDC', '自动建单、同步字段'),
             ('飞轮', '驱动工作项状态流转'), ('交付', '校验 + 邮件通知闭环')]
    for i, (a, b) in enumerate(nodes):
        cy = 200 + i * 120
        if i < 3:
            s.line([(880, cy + 40), (880, cy + 78)], color=C['brand'], sw=3)
        s.circle(880, cy, 40, fill=C['white'], stroke=C['brand'], sw=3)
        s.text(840, cy - 40, 80, 80, a, size=17, color=C['brand'], bold=True, align='c', valign='m', lh=1.0)
        s.text(940, cy - 20, 280, 40, b, size=17, color=C['text'], valign='m', lh=1.2)
    return s


# ------------------------------------------------------------------ 02 目录
def s02():
    s = frame(2, None, '目录')
    s.rect(60, 120, 1160, 56, fill=C['grayl'], rx=8)
    s.text(84, 120, 1120, 56, '{b#7B8794:00  前言}    先统一语言：RN的内容边界与“两个分身”',
           size=17, color=C['sub'], valign='m', lh=1.2)
    items = [
        (1, '痛点问题', ['国内已理顺，国际日益突出', '国际四大痛点']),
        (2, '原因分析', ['三年改进历程复盘', '根因：难在触发，断在传递']),
        (3, '解决方案', ['“搭车”主业务场景', '端到端流程与关键设计', '工具链落地进展']),
        (4, '成果收益', ['阶段成果与预期收益', '未来规划']),
    ]
    for i, (n, name, subs) in enumerate(items):
        x = 60 + i * 295
        _, c, cl = PARTS[n]
        s.rect(x, 205, 270, 330, fill=C['white'], stroke=C['line'], rx=10)
        s.rect(x, 205, 270, 8, fill=c)
        s.text(x + 28, 240, 220, 70, f'0{n}', size=56, color=c, bold=True, lh=1.1)
        s.text(x + 28, 325, 220, 40, name, size=26, color=C['navy'], bold=True, lh=1.2)
        s.rect(x + 28, 378, 40, 3, fill=c)
        s.text(x + 28, 400, 220, 130, subs, size=16, color=C['sub'], bullet='•', bullet_color=c, gap=10)
        if i < 3:
            s.poly([(x + 276, 360), (x + 290, 370), (x + 276, 380)], fill=C['line'])
    s.rect(60, 560, 1160, 100, fill=C['light'], rx=10)
    s.rect(60, 560, 6, 100, fill=C['brand'])
    s.text(90, 560, 1110, 100, '{b#0085CC:一句话概述：}三年改进发现，定制RN的核心困难在于需求触发；通过“搭车”iDOP升级主流程 + 工具链系统贯通，实现定制RN需求从触发、传递到交付的端到端闭环。',
           size=17, color=C['text'], valign='m', lh=1.55)
    return s


# ------------------------------------------------------------------ 03 RN的内容边界
def s03():
    s = frame(3, 0, 'RN的内容边界：本版本到底要说多少？',
              'RN即Release Notes（版本发布说明），是产品版本发布的“贴身说明书”。版本持续迭代N年，发布内容的边界如何划定？')
    cards = [
        ('从产品诞生至今的所有变更', '全量流水账', False, C['gray'], C['grayl'],
         ['小体量产品“小而美”，可行', '核心网all in one全融合产品体量大、历史久，滚雪球后维护和阅读体验都很差，通常不出此类RN']),
        ('基于上一个发布版本的更新', '通用RN', True, C['brand'], C['light'],
         ['随版本发布、打包在版本包中', '研发负责输出，作为版本发布必要条件纳入配置管理']),
        ('客户关注的内容', '定制RN', True, C['teal'], C['teall'],
         ['需求产生于版本升级场景', '不同客户关注点不同、现网升级梯度不同，必须量身定制']),
    ]
    for i, (q, name, ok, c, cl, pts) in enumerate(cards):
        x = 60 + i * 390
        s.rect(x, 135, 370, 290, fill=C['white'], stroke=C['line'], rx=10)
        s.rect(x, 135, 370, 96, fill=cl, rx=10)
        s.rect(x, 200, 370, 31, fill=cl)
        s.text(x + 24, 147, 320, 26, f'方案{"ABC"[i]}', size=14, color=c, bold=True, lh=1.2)
        s.text(x + 24, 175, 320, 44, q, size=19, color=C['navy'], bold=True, lh=1.25)
        (s.check if ok else s.cross)(x + 36, 262, 13, C['green'] if ok else C['red'])
        s.text(x + 58, 248, 290, 28, ('采用 → ' if ok else '不采用 · ') + name, size=18,
               color=c if ok else C['red'], bold=True, valign='m', lh=1.2)
        s.text(x + 24, 292, 325, 128, pts, size=15, color=C['sub'], bullet='•', bullet_color=c, gap=8)
    # 客户两个疑问
    s.rect(60, 445, 1160, 228, fill=C['teall'], rx=10)
    s.text(84, 460, 600, 28, '为什么必须定制？升级场景下客户的两个疑问', size=17, color=C['teal'], bold=True, lh=1.2)
    qs = [('Q1  为什么要升级？本次升级给我带来哪些业务价值？',
           '需了解：客户关注的业务价值点——市场承诺的新业务？还是需要解决的版本漏洞？'),
          ('Q2  新版本和我的上一个版本有哪些差别？新在哪里？',
           '需了解：客户的上一个版本是什么？涉及几个发布版本梯度？')]
    for i, (q, a) in enumerate(qs):
        x = 84 + i * 568
        s.rect(x, 500, 544, 155, fill=C['white'], rx=8)
        s.text(x + 18, 514, 510, 50, q, size=17, color=C['navy'], bold=True, lh=1.4)
        s.rect(x + 18, 570, 36, 3, fill=C['teal'])
        s.text(x + 18, 582, 510, 64, a, size=15, color=C['sub'], lh=1.5)
    return s


# ------------------------------------------------------------------ 04 RN的两个分身
def s04():
    s = frame(4, 0, '先统一语言：RN的两个分身', '通用RN回答“版本变了什么”，定制RN回答“这次升级对我意味着什么”')
    x0, x1, x2, xe = 60, 230, 725, 1220
    s.rect(x1, 130, x2 - x1 - 6, 56, fill=C['brand'], rx=8)
    s.rect(x2, 130, xe - x2, 56, fill=C['teal'], rx=8)
    s.text(x1, 130, x2 - x1 - 6, 56, '通用RN  ·  随版本发布的迭代变更RN', size=18, color=C['white'], bold=True, align='c', valign='m', lh=1.2)
    s.text(x2, 130, xe - x2, 56, '定制RN  ·  按客户需求定制的RN', size=18, color=C['white'], bold=True, align='c', valign='m', lh=1.2)
    rows = [
        ('定位', '版本发布的迭代变更说明', '按客户需求量身定制的版本说明'),
        ('内容基线', '基于上一个发布版本的更新', '客户现网版本 → 目标版本，可能跨越多个发布梯度'),
        ('文档属性', '研发交付的产品文档', '现场交付的工程文档'),
        ('责任归属', '研发负责输出，纳入配置管理，作为版本发布必要条件', '需求驱动编制（后方承诺承接编制任务）'),
        ('获取渠道', '直接从Support获取', '需提交需求，通过需求传递渠道获取'),
        ('适用边界', '无市场差异性处理，未经市场和交付干系人审核，不能直接提供给客户',
         '聚焦客户关注的业务价值点与版本差异，直接服务升级沟通'),
    ]
    y = 198
    for i, (k, a, b) in enumerate(rows):
        rh = 78
        fill = C['light2'] if i % 2 == 0 else C['white']
        s.rect(x0, y, xe - x0, rh, fill=fill)
        s.text(x0 + 16, y, x1 - x0 - 24, rh, k, size=16, color=C['navy'], bold=True, valign='m', lh=1.2)
        s.text(x1 + 20, y, x2 - x1 - 46, rh, a, size=15.5, color=C['text'], valign='m', lh=1.4)
        s.text(x2 + 20, y, xe - x2 - 40, rh, b, size=15.5, color=C['text'], valign='m', lh=1.4)
        y += rh
    s.line([(x0, y), (xe, y)], color=C['line'], sw=1, arrow=False)
    return s


# ------------------------------------------------------------------ 05 痛点全景
def s05():
    s = frame(5, 1, '痛点全景：国内已理顺，国际问题日益突出')
    # 左：国内 vs 国际
    s.rect(60, 125, 290, 245, fill=C['greenl'], rx=10)
    s.check(88, 154, 13, C['green'])
    s.text(110, 140, 220, 28, '国内 · 已理顺', size=19, color=C['green'], bold=True, valign='m', lh=1.2)
    s.text(78, 180, 258, 185, ['问题最早来自国内营销反馈', 'V7普及、版本统一，升级梯度相对统一',
                               '按运营商节奏，每年一份即可', '交付项目组牵头、产品线整理，协作渐入正轨',
                               '近几年已不再反馈'],
           size=14, color=C['text'], bullet='•', bullet_color=C['green'], gap=4, lh=1.35)
    s.rect(60, 385, 290, 285, fill=C['redl'], rx=10)
    s.cross(88, 414, 13, C['red'])
    s.text(110, 400, 220, 28, '国际 · 日益突出', size=19, color=C['red'], bold=True, valign='m', lh=1.2)
    s.text(78, 440, 258, 220, ['交付涉及人员众多', 'CCN文档团队持续推进改进，但过程并不顺利',
                               '磕磕绊绊，已有三年', '集中表现为右侧四大痛点'],
           size=14, color=C['text'], bullet='•', bullet_color=C['red'], gap=6, lh=1.35)
    s.line([(350, 527), (372, 527)], color=C['red'], sw=2.5)
    # 右：四大痛点
    cards = [
        (1, '语言不统一', '共识推进中', C['orange'], C['orangel'],
         ['后方：通用RN属研发产品文档，定制RN属现场工程文档，概念、生产过程、职责归属是两条线',
          '国际交付涉及人员众多，概念区分难以普及']),
        (2, '交付职责拉扯', '已磨合', C['orange'], C['orangel'],
         ['国际：文档内外合一，Support上的RN应可直接（或轻量裁剪后）交付客户',
          '后方：通用RN未经市场和交付审核，不能直接给客户；定制RN应对齐国内，由现场项目组牵头']),
        (3, '通用RN英化有过硬伤', '已改善', C['green'], C['greenl'],
         ['早期研发人工翻译，水平参差、缺乏质保，前方反馈过低级拼写错误',
          '现已推广translate机翻、CCN专用词库、拼写检查纳入DevOps流水线']),
        (4, '需求传递不畅', '核心难题', C['red'], C['redl'],
         ['定制RN需求与现场工程操作紧密相关，理想是在工程操作前甄别并提出',
          '需求未提、提交滞后、提交后不能及时传递到产研的情况仍然存在']),
    ]
    for i, (n, t, tag, c, cl, pts) in enumerate(cards):
        x = 385 + (i % 2) * 425
        y = 125 + (i // 2) * 232
        hl = n == 4
        s.rect(x, y, 410, 218, fill=C['white'], stroke=C['red'] if hl else C['line'], sw=2.5 if hl else 1, rx=10)
        s.num(x + 30, y + 30, n, C['red'], r=15)
        s.text(x + 54, y + 14, 240, 32, t, size=19, color=C['navy'], bold=True, valign='m', lh=1.2)
        s.rect(x + 300, y + 17, 92, 26, fill=cl, rx=13)
        s.text(x + 300, y + 17, 92, 26, tag, size=13, color=c, bold=True, align='c', valign='m', lh=1.0)
        s.text(x + 22, y + 58, 370, 155, pts, size=14, color=C['sub'], bullet='•', bullet_color=C['red'], gap=6, lh=1.4)
    s.rect(385, 590, 835, 80, fill=C['redl'], rx=10)
    s.text(410, 590, 790, 80, '痛点1~3通过前后方沟通磨合与工具改善已逐步缓解；{b#D9483B:痛点4“需求传递不畅”是三年改进始终未解的核心难题}，也是本专项的主攻方向。',
           size=16, color=C['text'], valign='m', lh=1.45)
    return s


# ------------------------------------------------------------------ 06 三年改进历程
def s06():
    s = frame(6, 2, '三年改进历程：每一步都卡在“需求”上', 'CCN文档团队自2024年起将国际定制RN作为改进专项推进')
    cols = [250, 575, 900]
    cw = 310
    s.rect(250, 150, 970, 7, fill=C['sub'])
    s.poly([(1215, 140), (1240, 153.5), (1215, 167)], fill=C['sub'])
    for x, (yr, name) in zip(cols, [('2024年', '统一思想'), ('2025年', '流程上线'), ('2026年', '断点接续')]):
        cx = x + cw / 2
        s.text(cx - 80, 116, 160, 30, yr, size=20, color=C['navy'], bold=True, align='c', valign='m', lh=1.0)
        s.circle(cx, 153.5, 9, fill=C['brand'], stroke=C['white'], sw=3)
        s.line([(cx, 163), (cx, 180)], color=C['brand'], sw=1.5, dash=True, arrow=False)
        s.rect(x, 180, cw, 36, fill=C['brand'], rx=4)
        s.text(x, 180, cw, 36, name, size=18, color=C['white'], bold=True, align='c', valign='m', lh=1.0)
    s.chevron(60, 200, 175, 170, C['brand'], first=True)
    s.text(72, 200, 140, 170, '定制RN：\n{b:线上流程打通}', size=17, color=C['white'], valign='m', lh=1.45)
    s.chevron(60, 395, 175, 90, C['gray'], first=True)
    s.text(72, 395, 140, 90, '通用RN：\n{b:基础能力打底}', size=17, color=C['white'], valign='m', lh=1.45)
    custom = [
        ['国际工服文档团队接纳定制RN需求提交要求', '确定定制RN的流程和职责', '国际组织试点触发定制RN需求提交{b#D9483B:（效果不佳1）}'],
        ['研发RDC上线ER工作项支持工程验证需求', 'RDC-ER支持定制RN需求标识{b#D9483B:（效果不佳2）}', '{b#0085CC:提出定制RN需求搭车iDOP模型包验证流程}'],
        ['iDOP上线定制RN需求字段', 'H1收集到定制RN需求30+{b#D9483B:（未传递到研发RDC）}', 'iDOP和RDC系统打通，实现自动创建ER并传递需求（8月中上线）'],
    ]
    generic = ['研发通用RN提质提效实践探索', 'USPP完成通用RN自动生成实践探索，极大提高通用RN生产效率', 'CCN中心横推通用RN自动生成实践']
    for x, cu, ge in zip(cols, custom, generic):
        s.rect(x, 216, cw, 160, fill=C['white'], stroke='#8CC8EA', sw=1.2)
        s.text(x + 16, 226, cw - 30, 145, cu, size=14, color=C['text'], bullet='•', bullet_color=C['brand'], gap=5, lh=1.38)
        s.rect(x, 395, cw, 90, fill=C['grayl'], stroke=C['line'])
        s.text(x + 16, 403, cw - 30, 76, [ge], size=14, color=C['sub'], bullet='•', bullet_color=C['gray'], lh=1.38, valign='m')
    # 问题复盘
    s.chevron(60, 505, 175, 165, C['red'], first=True)
    s.text(72, 505, 140, 165, '问题复盘：\n{b:三个断点}', size=17, color=C['white'], valign='m', lh=1.45)
    notes = [('效果不佳1', '约定的ZXRDC提交定制RN需求，很难落地，鲜有提交，靠人盯人，很难持续。'),
             ('效果不佳2', '虽然研发RDC有定制RN需求字段触发后端文档生产流程，但没有需求数据来源，ER提交者非定制RN直接干系人，难以识别。'),
             ('iDOP需求未能传递到RDC', '典型的工作流断链，通过工具开发支持系统贯通是终极方案。')]
    for x, (t, d) in zip(cols, notes):
        s.rect(x, 505, cw, 165, fill=C['redl'], rx=6)
        s.rect(x, 505, 5, 165, fill=C['red'])
        s.text(x + 20, 515, cw - 34, 28, t, size=16, color=C['red'], bold=True, valign='m', lh=1.2)
        s.text(x + 20, 548, cw - 34, 118, d, size=14, color=C['text'], lh=1.45)
    return s


# ------------------------------------------------------------------ 07 根因分析
def s07():
    s = frame(7, 2, '根因分析：难在“触发”，断在“传递”',
              '三年摸索的结论：定制RN的核心困难是①如何触发需求识别？②需求触发后如何传递和闭环？')
    for x, w, t, c in [(60, 330, '现象（三个断点）', C['red']), (450, 400, '根因', C['orange']), (910, 310, '本质', C['navy'])]:
        s.text(x, 124, w, 26, t, size=15, color=c, bold=True, lh=1.2)
    phen = [('效果不佳1', 'ZXRDC单独提交定制RN需求，鲜有提交，靠人盯人'),
            ('效果不佳2', 'RDC有定制RN需求字段，却没有需求数据来源'),
            ('断链', 'iDOP收集到30+需求，未能传递到研发RDC')]
    roots = [('R1  定制RN不是主业务场景', '单独提交的要求游离于工程交付主流程之外，执行起来不是遗漏，就是滞后'),
             ('R2  需求源头错位', 'ER提交者并非定制RN直接干系人，需求难以识别'),
             ('R3  工具链断链', 'iDOP与RDC系统未贯通，需求无法自动流转')]
    ys = [155, 305, 455]
    for y, (t, d), (rt, rd) in zip(ys, phen, roots):
        s.rect(60, y, 330, 130, fill=C['redl'], rx=8)
        s.text(80, y + 14, 290, 26, t, size=17, color=C['red'], bold=True, lh=1.2)
        s.text(80, y + 48, 290, 75, d, size=15, color=C['text'], lh=1.45)
        s.line([(392, y + 65), (446, y + 65)], color=C['red'], sw=2.5)
        s.rect(450, y, 400, 130, fill=C['orangel'], rx=8)
        s.text(470, y + 14, 360, 26, rt, size=17, color=C['orange'], bold=True, lh=1.2)
        s.text(470, y + 48, 360, 75, rd, size=15, color=C['text'], lh=1.45)
    # 本质
    s.rect(910, 155, 310, 280, fill=C['red'], rx=10)
    s.text(935, 175, 260, 36, '需求触发难', size=26, color=C['white'], bold=True, lh=1.2)
    s.rect(935, 220, 60, 3, fill=C['white'])
    s.text(935, 238, 262, 190, ['最困难的环节', '定制RN在工程交付中不是主业务场景，单独提需求难以落地'],
           size=15.5, color=C['white'], bullet='•', gap=8, lh=1.45)
    s.rect(910, 455, 310, 130, fill=C['orange'], rx=10)
    s.text(935, 470, 260, 34, '需求传递断', size=24, color=C['white'], bold=True, lh=1.2)
    s.text(935, 508, 270, 70, '识别到断点后，解决只是资源和时间问题', size=15.5, color=C['white'], lh=1.45)
    s.line([(852, 220), (906, 260)], color=C['orange'], sw=2.5)
    s.line([(852, 370), (906, 330)], color=C['orange'], sw=2.5)
    s.line([(852, 520), (906, 520)], color=C['orange'], sw=2.5)
    s.rect(60, 605, 1160, 66, fill=C['brand'], rx=10)
    s.text(84, 605, 1112, 66, '破题思路：{b:触发靠“搭车”主业务场景，传递靠工具链系统贯通}',
           size=20, color=C['white'], align='c', valign='m', lh=1.2)
    return s


# ------------------------------------------------------------------ 08 搭车策略
def s08():
    s = frame(8, 3, '核心策略：“搭车”主业务场景，一次勾选触发需求',
              '理解业务本质：定制RN不是工程交付的主业务场景，与其另起炉灶，不如搭载必经的主流程')
    # 左：过去
    s.rect(60, 130, 360, 540, fill=C['grayl'], rx=10)
    s.text(84, 145, 300, 30, '过去：单独提交', size=19, color=C['gray'], bold=True, valign='m', lh=1.2)
    steps = [('交付人员完成升级等工程操作', C['white'], C['text']),
             ('额外到ZXRDC单独提交定制RN需求', C['white'], C['text']),
             ('不是遗漏，就是滞后\n靠人盯人，难以持续', C['redl'], C['red'])]
    y = 200
    for i, (t, f, c) in enumerate(steps):
        s.box(90, y, 300, 88, t, fill=f, stroke=C['line'] if i < 2 else C['red'], color=c, size=16, bold=i == 2)
        if i < 2:
            s.line([(240, y + 88), (240, y + 122)], color=C['gray'], sw=2)
            if i == 1:
                s.text(250, y + 92, 150, 26, '非主流程 · 易忽略', size=13, color=C['red'], valign='m', lh=1.0)
        y += 125
    s.cross(240, 600, 18, C['red'])
    s.text(90, 625, 300, 30, '落地难', size=16, color=C['red'], bold=True, align='c', valign='m', lh=1.0)
    s.poly([(436, 380), (466, 400), (436, 420)], fill=C['brand'])
    # 右：搭车
    s.rect(480, 130, 740, 540, fill=C['light'], rx=10)
    s.text(504, 145, 600, 30, '现在：搭车外场升级主流程（iDOP）', size=19, color=C['brand'], bold=True, valign='m', lh=1.2)
    s.rect(505, 320, 690, 5, fill=C['deep'])
    s.poly([(1190, 312), (1210, 322.5), (1190, 333)], fill=C['deep'])
    cars = [('iDOP\n升级方案申请', False), ('方案模型开发', False), ('模型包验证', False), ('是否需要\n定制RN', True)]
    for i, (t, hl) in enumerate(cars):
        x = 515 + i * 168
        f = C['brand'] if hl else C['white']
        s.rect(x, 205, 148, 100, fill=f, stroke=C['brand'], sw=2, rx=10)
        if hl:
            s.rect(x + 14, 220, 22, 22, fill=C['white'], rx=3)
            s.line([(x + 18, 231), (x + 24, 237), (x + 33, 224)], color=C['brand'], sw=3, arrow=False)
            s.text(x + 40, 210, 102, 90, t, size=16, color=C['white'], bold=True, align='c', valign='m', lh=1.3)
        else:
            s.text(x + 8, 210, 132, 90, t, size=16, color=C['navy'], bold=True, align='c', valign='m', lh=1.3)
        for wx in (x + 35, x + 113):
            s.circle(wx, 313, 9, fill=C['deep'])
        if i < 3:
            s.rect(x + 148, 252, 20, 6, fill=C['deep'])
    s.text(1020, 168, 175, 30, '搭载的“一节车厢”', size=14, color=C['brand'], bold=True, align='c', valign='m', lh=1.0)
    s.text(515, 345, 650, 26, '主业务列车：外场升级必经流程', size=14, color=C['deep'], valign='m', lh=1.0)
    insights = [('场景吻合', '定制RN的需求场景基本都产生在升级场景'),
                ('必经之路', '外场升级需在iDOP申请方案模型开发及模型包验证'),
                ('用户友好', '只在主业务申请时做一次“是否需要定制RN”勾选')]
    for i, (t, d) in enumerate(insights):
        x = 505 + i * 233
        s.rect(x, 380, 220, 185, fill=C['white'], rx=10)
        s.num(x + 34, 414, i + 1, C['brand'], r=17, size=17)
        s.text(x + 60, 399, 150, 30, t, size=19, color=C['navy'], bold=True, valign='m', lh=1.2)
        s.text(x + 20, 448, 182, 110, d, size=16, color=C['sub'], lh=1.55)
    s.rect(505, 582, 690, 68, fill=C['brand'], rx=10)
    s.text(525, 582, 650, 68, '需求触发从“靠自觉、靠人盯”变为“必经流程、顺手勾选”',
           size=18, color=C['white'], bold=True, align='c', valign='m', lh=1.3)
    return s


# ------------------------------------------------------------------ 09 端到端流程
def s09():
    s = frame(9, 3, '端到端流程：从iDOP勾选到客户交付，全程系统贯通')
    stages = [('① 需求触发', '交付总工', C['teal']), ('② 定制RN开发', '研发工程文档负责人', C['brand']),
              ('③ 定制RN评审', '研发工程文档负责人', C['brand']), ('④ 定制RN发布', '研发工程文档负责人', C['brand']),
              ('⑤ 客户交付', '交付项目TD', C['deep'])]
    for i, (t, r, c) in enumerate(stages):
        x = 60 + i * 232
        s.chevron(x, 118, 240, 64, c, first=i == 0)
        s.text(x + (18 if i == 0 else 30), 120, 190, 60, f'{{b:{t}}}\n{r}', size=14.5, color=C['white'],
               align='c', valign='m', lh=1.35)
    # 触发阶段：系统自动建单
    s.text(60, 194, 520, 24, '触发阶段 · 系统自动建单', size=15, color=C['teal'], bold=True, valign='m', lh=1.0)
    by, bh = 225, 86
    s.box(60, by, 200, bh, '{b:iDOP}\n方案中心·方案模型开发', fill=C['teall'], stroke=C['teal'], size=14.5, lh=1.35)
    s.line([(262, by + bh / 2), (296, by + bh / 2)], color=C['sub'], sw=2)
    s.box(300, by, 200, bh, '{b:RDC-ER}\n自动创建ER单\n同步字段A/B/C', fill=C['teall'], stroke=C['teal'], size=14.5, lh=1.3)
    s.line([(502, by + bh / 2), (536, by + bh / 2)], color=C['sub'], sw=2)
    s.diamond(620, by + bh / 2, 164, 92, '是否\n定制RN', size=14.5)
    s.line([(702, by + bh / 2), (746, by + bh / 2)], color=C['sub'], sw=2)
    s.text(706, by + 14, 40, 22, '是', size=13, color=C['green'], bold=True, align='c', valign='m', lh=1.0)
    s.text(630, by + bh / 2 + 46, 120, 22, '否：不触发', size=12.5, color=C['mute'], valign='m', lh=1.0)
    s.box(750, by, 210, bh, '读配置\n写入“定制RN作者”', fill=C['beige'], stroke=C['orange'], size=14.5, lh=1.35)
    s.line([(962, by + bh / 2), (996, by + bh / 2)], color=C['sub'], sw=2)
    s.box(1000, by, 220, bh, '{b:飞轮}\n创建RDC文档工作项', fill=C['brand'], color=C['white'], size=15, lh=1.35)
    # ABC 字段
    s.rect(60, 322, 480, 42, fill=C['redl'], rx=6)
    s.text(74, 322, 460, 42, '勾选字段：{b#D9483B:A} 是否定制RN   {b#D9483B:B} 定制RN是否英化   {b#D9483B:C} 定制RN具体需求',
           size=13.5, color=C['text'], valign='m', lh=1.2)
    # 状态流转带
    s.line([(1110, by + bh), (1110, 392), (130, 392), (130, 478)], color=C['brand'], sw=2.2)
    s.rect(60, 410, 1160, 190, fill=C['beige'], rx=10)
    s.text(780, 418, 425, 26, 'RDC文档工作项 · 状态翻转由飞轮控制', size=15, color=C['orange'], bold=True,
           align='r', valign='m', lh=1.0)
    states = ['新建', '开始\n内容开发', '完成\n内容开发', '开始\n评审', '评审\n通过', '可交付', '已交付']
    xs = [130 + i * 170 for i in range(7)]
    for i, (cx, st) in enumerate(zip(xs, states)):
        s.circle(cx, 512, 36, fill=C['white'], stroke=C['brand'], sw=2.2)
        s.text(cx - 34, 478, 68, 68, st, size=13, color=C['navy'], bold=True, align='c', valign='m', lh=1.25)
        if i < 6:
            s.line([(cx + 37, 512), (cx + 131, 512)], color=C['brand'], sw=2)
    groups = [(0, 2, '② 开发：文档编写任务驱动'), (3, 4, '③ 评审：文档评审任务驱动'),
              (5, 5, '④ 发布：附件校验'), (6, 6, '⑤ 交付')]
    for a, b, t in groups:
        x1, x2 = xs[a] - 60, xs[b] + 60
        s.rect(x1, 560, x2 - x1, 5, fill=C['orange'], rx=2)
        s.text(x1, 568, x2 - x1, 24, t, size=13, color=C['orange'], bold=True, align='c', valign='m', lh=1.0)
    notes = [('任务驱动', '文档编写/评审任务的Active、Closed状态自动翻转工作项状态，无需人工推进'),
             ('自动闭环', '附件与英化自动校验通过即“可交付”，飞轮邮件通知需求提交人（中英双语）')]
    for i, (t, d) in enumerate(notes):
        x = 60 + i * 590
        s.rect(x, 612, 570, 60, fill=C['light'], rx=8)
        s.text(x + 18, 612, 540, 60, f'{{b#0085CC:{t}}}  {d}', size=14, color=C['text'], valign='m', lh=1.4)
    return s


# ------------------------------------------------------------------ 10 关键设计
def s10():
    s = frame(10, 3, '关键设计：任务驱动状态流转，质量门禁自动校验')
    regions = [(60, 470, C['brand']), (500, 800, C['brand']), (830, 1030, C['orange']), (1060, 1220, C['green'])]
    xs = [115, 265, 415, 580, 720, 930, 1140]
    states = ['新建', '开始\n内容开发', '完成\n内容开发', '开始\n评审', '评审\n通过', '可交付', '已交付']
    s.rect(60, 120, 1160, 110, fill=C['light2'], rx=10)
    for i, (cx, st) in enumerate(zip(xs, states)):
        c = C['orange'] if i == 5 else (C['green'] if i == 6 else C['brand'])
        s.circle(cx, 175, 34, fill=C['white'], stroke=c, sw=2.2)
        s.text(cx - 32, 143, 64, 64, st, size=12.5, color=C['navy'], bold=True, align='c', valign='m', lh=1.25)
        if i < 6:
            s.line([(cx + 35, 175), (xs[i + 1] - 37, 175)], color=C['gray'], sw=1.8)
    for (x1, x2, c), cx in zip(regions, [265, 650, 930, 1140]):
        s.line([(cx, 211), (cx, 254)], color=c, sw=1.5, dash=True)
    # A 编写任务
    def card(x1, x2, title, c, cl):
        s.rect(x1, 258, x2 - x1, 412, fill=C['white'], stroke=C['line'], rx=10)
        s.rect(x1, 258, x2 - x1, 44, fill=cl, rx=10)
        s.rect(x1, 286, x2 - x1, 16, fill=cl)
        s.text(x1 + 16, 258, x2 - x1 - 32, 44, title, size=16, color=c, bold=True, valign='m', lh=1.2)

    card(60, 470, '文档编写任务 → 驱动开发状态', C['brand'], C['light'])
    rows = [('Active', C['brand'], '工作项翻转为“开始内容开发”'),
            ('Closed', C['green'], '校验“文档任务输出字段链接”有效 → “完成内容开发”'),
            ('Removed', C['red'], '任务被移除 → 退回重新创建编写任务')]
    for i, (tag, c, d) in enumerate(rows):
        y = 325 + i * 110
        s.rect(80, y, 92, 30, fill=c, rx=15)
        s.text(80, y, 92, 30, tag, size=14, color=C['white'], bold=True, align='c', valign='m', lh=1.0)
        s.line([(176, y + 15), (200, y + 15)], color=C['gray'], sw=1.8)
        s.text(206, y - 4, 248, 80, d, size=15, color=C['text'], lh=1.45)
    card(500, 800, '文档评审任务 → 驱动评审状态', C['brand'], C['light'])
    rows = [('Active', C['brand'], '工作项翻转为\n“开始评审”'), ('Closed', C['green'], '工作项翻转为\n“评审通过”')]
    for i, (tag, c, d) in enumerate(rows):
        y = 325 + i * 110
        s.rect(520, y, 92, 30, fill=c, rx=15)
        s.text(520, y, 92, 30, tag, size=14, color=C['white'], bold=True, align='c', valign='m', lh=1.0)
        s.line([(616, y + 15), (640, y + 15)], color=C['gray'], sw=1.8)
        s.text(646, y - 4, 145, 70, d, size=15, color=C['text'], lh=1.45)
    s.rect(520, 555, 262, 100, fill=C['light2'], rx=8)
    s.text(536, 563, 232, 86, '状态翻转由飞轮自动控制，作者只需处理自己的任务，进度实时可见',
           size=14, color=C['sub'], lh=1.5, valign='m')
    # C 交付门禁
    card(830, 1030, '交付门禁 · 自动校验', C['orange'], C['orangel'])
    s.box(845, 312, 170, 50, '提交附件到工作项“描述”', fill=C['beige'], stroke=C['orange'], size=13, lh=1.3)
    s.line([(930, 362), (930, 378)], color=C['gray'], sw=1.8)
    s.diamond(930, 412, 170, 66, '描述字段\n有附件？', size=13)
    s.line([(930, 445), (930, 462)], color=C['gray'], sw=1.8)
    s.text(936, 444, 30, 18, '是', size=12, color=C['green'], bold=True, valign='m', lh=1.0)
    s.diamond(930, 496, 170, 66, '定制RN\n是否英化？', size=13)
    s.line([(930, 529), (930, 546)], color=C['gray'], sw=1.8)
    s.text(936, 528, 30, 18, '是', size=12, color=C['green'], bold=True, valign='m', lh=1.0)
    s.diamond(930, 580, 170, 66, '附件为\n英文？', size=13)
    s.line([(930, 613), (930, 626)], color=C['gray'], sw=1.8)
    s.box(870, 628, 120, 34, '可交付', fill=C['green'], color=C['white'], size=14, bold=True, rx=17)
    s.line([(1015, 496), (1022, 496), (1022, 645), (992, 645)], color=C['green'], sw=1.5)
    s.text(1000, 474, 28, 18, '否', size=12, color=C['green'], bold=True, align='c', valign='m', lh=1.0)
    s.text(834, 382, 44, 30, '否退回', size=12, color=C['red'], bold=True, valign='m', lh=1.0)
    s.text(834, 550, 44, 30, '否退回', size=12, color=C['red'], bold=True, valign='m', lh=1.0)
    # D 邮件通知
    card(1060, 1220, '邮件通知 · 闭环', C['green'], C['greenl'])
    s.rect(1110, 322, 60, 42, fill=C['white'], stroke=C['green'], sw=2, rx=4)
    s.line([(1110, 324), (1140, 346), (1170, 324)], color=C['green'], sw=2, arrow=False)
    s.text(1074, 378, 134, 70, '飞轮给项目负责人发邮件，通知需求提交人任务完成', size=13.5, color=C['text'], lh=1.45)
    s.rect(1074, 462, 134, 196, fill=C['greenl'], rx=6)
    s.text(1084, 470, 116, 182, '“您提交的定制ReleaseNotes需求（用户文档标识链接）任务已完成，请联系“定制RN作者”获取。”\n{b#1F9D6B:中英双语}',
           size=12.5, color=C['sub'], lh=1.45)
    return s


# ------------------------------------------------------------------ 11 落地进展
def s11():
    s = frame(11, 3, '落地进展：方案已评审，工具链需求全面提交',
              '端到端流程方案已通过评审，已向RDC、飞轮、iDOP等工具链系统提交需求，预计26年Q3全流程贯通')
    ms = [(True, '端到端流程方案通过评审', '理解业务本质与全流程操作后完善设计'),
          (True, '向RDC、飞轮、iDOP提交工具链需求', '三个系统同步立项改造'),
          (True, 'iDOP上线定制RN需求字段', '升级方案申请时即可勾选'),
          (True, 'H1收集到定制RN需求30+', '“搭车”触发初见成效，但尚未传递到研发RDC'),
          (False, 'iDOP和RDC系统打通（8月中上线）', '自动创建ER并传递需求，接续断点'),
          (False, '定制RN全流程贯通（预计26年Q3）', '触发→传递→生产→交付端到端闭环')]
    s.text(60, 126, 300, 26, '里程碑', size=17, color=C['navy'], bold=True, lh=1.2)
    s.line([(90, 175), (90, 640)], color=C['line'], sw=3, arrow=False)
    for i, (done, t, d) in enumerate(ms):
        y = 175 + i * 93
        if done:
            s.check(90, y, 14, C['green'])
        else:
            s.circle(90, y, 14, fill=C['white'], stroke=C['brand'], sw=3)
            s.circle(90, y, 5, fill=C['brand'])
        s.text(120, y - 16, 500, 28, t, size=17, color=C['navy'] if done else C['brand'], bold=True, valign='m', lh=1.2)
        s.text(120, y + 13, 500, 24, d, size=14, color=C['sub'], valign='m', lh=1.2)
    s.check(430, 140, 8, C['green'])
    s.text(444, 130, 60, 20, '已完成', size=12, color=C['sub'], valign='m', lh=1.0)
    s.circle(520, 140, 8, fill=C['white'], stroke=C['brand'], sw=2.5)
    s.text(534, 130, 60, 20, '推进中', size=12, color=C['sub'], valign='m', lh=1.0)
    s.text(680, 126, 400, 26, '三大系统分工', size=17, color=C['navy'], bold=True, lh=1.2)
    systems = [('iDOP', '需求入口', C['teal'], C['teall'], '方案中心·方案模型开发申请时勾选A/B/C三个定制RN需求字段'),
               ('RDC', '需求承接', C['brand'], C['light'], 'ER自动创建并同步字段；判断是否定制RN，读配置写入“定制RN作者”；承载文档工作项'),
               ('飞轮', '流程引擎', C['deep'], '#E1ECF3', '创建RDC文档工作项，按任务状态控制状态翻转，可交付时发送邮件通知')]
    for i, (n, role, c, cl, d) in enumerate(systems):
        y = 165 + i * 168
        s.rect(680, y, 540, 150, fill=cl, rx=10)
        s.rect(680, y, 130, 150, fill=c, rx=10)
        s.rect(780, y, 30, 150, fill=c)
        s.text(680, y + 30, 130, 50, n, size=26, color=C['white'], bold=True, align='c', valign='m', lh=1.0)
        s.text(680, y + 82, 130, 30, role, size=15, color=C['white'], align='c', valign='m', lh=1.0)
        s.text(832, y + 12, 370, 126, d, size=16, color=C['text'], valign='m', lh=1.55)
    return s


# ------------------------------------------------------------------ 12 成果收益
def s12():
    s = frame(12, 4, '成果收益：定制RN需求从“靠人盯”走向“系统转”')
    s.text(60, 120, 400, 28, '阶段成果', size=18, color=C['green'], bold=True, valign='m', lh=1.2)
    s.rect(60, 155, 400, 205, fill=C['green'], rx=12)
    s.text(84, 165, 360, 90, '30+', size=72, color=C['white'], bold=True, lh=1.1, valign='m')
    s.text(84, 258, 360, 30, '2026年H1通过iDOP收集的定制RN需求', size=16, color=C['white'], bold=True, lh=1.2)
    s.text(84, 292, 360, 56, '对比此前单独到ZXRDC提交“鲜有提交”，“搭车”策略有效解决了需求触发难题',
           size=14, color='#DDF3EA', lh=1.45)
    wins = [('语言统一', '国际工服文档团队接纳“定制RN需提需求”的理念'),
            ('职责明确', '后方承诺承接定制RN编制，流程和职责已确定'),
            ('质量提效', '机翻+专用词库+拼写检查保障英化质量；通用RN自动生成大幅提效')]
    for i, (t, d) in enumerate(wins):
        y = 375 + i * 100
        s.rect(60, y, 400, 88, fill=C['greenl'], rx=10)
        s.check(88, y + 26, 12, C['green'])
        s.text(108, y + 12, 330, 28, t, size=16.5, color=C['green'], bold=True, valign='m', lh=1.2)
        s.text(80, y + 42, 365, 44, d, size=14, color=C['text'], lh=1.4)
    # 右：前后对比
    s.text(500, 120, 500, 28, '预期收益：全流程贯通后的改进前后对比', size=18, color=C['green'], bold=True, valign='m', lh=1.2)
    xk, xb, xa, xe = 500, 630, 920, 1220
    s.rect(xk, 155, xe - xk, 44, fill=C['navy'], rx=6)
    s.text(xk + 14, 155, 110, 44, '环节', size=15, color=C['white'], bold=True, valign='m', lh=1.0)
    s.text(xb + 14, 155, 260, 44, '改进前', size=15, color=C['white'], bold=True, valign='m', lh=1.0)
    s.text(xa + 14, 155, 280, 44, '改进后', size=15, color=C['white'], bold=True, valign='m', lh=1.0)
    rows = [('需求触发', '单独到ZXRDC提交，靠人盯人', '搭车iDOP升级流程，一次勾选'),
            ('需求识别', 'ER提交者非直接干系人，难以识别', '交付总工在源头勾选A/B/C字段'),
            ('需求传递', 'iDOP需求无法传递到RDC，断链', '系统贯通，自动建单、同步字段'),
            ('过程管控', '依赖人工跟踪，难以持续', '飞轮驱动状态翻转，全程可追溯'),
            ('交付闭环', '交付结果依赖人工确认', '附件/英化自动校验，邮件通知闭环')]
    for i, (k, b, a) in enumerate(rows):
        y = 205 + i * 93
        s.rect(xk, y, xe - xk, 87, fill=C['light2'] if i % 2 == 0 else C['white'], rx=6)
        s.text(xk + 14, y, 110, 87, k, size=16, color=C['navy'], bold=True, valign='m', lh=1.2)
        s.cross(xb + 20, y + 43.5, 10, '#B9C2CB')
        s.text(xb + 40, y, 240, 87, b, size=15, color=C['mute'], valign='m', lh=1.4)
        s.line([(xa - 18, y + 43.5), (xa + 2, y + 43.5)], color=C['green'], sw=2.5)
        s.check(xa + 24, y + 43.5, 10, C['green'])
        s.text(xa + 44, y, 250, 87, a, size=15, color=C['text'], bold=True, valign='m', lh=1.4)
    return s


# ------------------------------------------------------------------ 13 未来规划
def s13():
    s = frame(13, 4, '未来规划：聚焦内容，从“快”到“又快又好”',
              '完成定制RN流程改进后，后续RN改进仍聚焦内容')
    # 左：二维示意
    ox, oy, aw, ah = 120, 620, 470, 440
    s.rect(ox, oy - ah, aw, ah, fill=C['light2'])
    s.rect(ox + aw / 2, oy - ah, aw / 2, ah / 2, fill=C['greenl'])
    s.line([(ox, oy), (ox + aw + 20, oy)], color=C['sub'], sw=2)
    s.line([(ox, oy), (ox, oy - ah - 20)], color=C['sub'], sw=2)
    s.text(ox + aw - 200, oy + 8, 220, 24, '生产效率（快）→', size=14, color=C['sub'], bold=True, align='r', valign='m', lh=1.0)
    s.text(ox + 10, oy - ah - 22, 240, 22, '↑ 客户可读性（好）', size=14, color=C['sub'], bold=True, valign='m', lh=1.0)
    s.line([(ox + aw / 2, oy), (ox + aw / 2, oy - ah)], color=C['line'], sw=1, dash=True, arrow=False)
    s.line([(ox, oy - ah / 2), (ox + aw, oy - ah / 2)], color=C['line'], sw=1, dash=True, arrow=False)
    s.text(ox + aw / 2 + 12, oy - ah + 12, 220, 24, '目标区：又快又好', size=14, color=C['green'], bold=True, valign='m', lh=1.0)
    cur = (ox + aw * 0.78, oy - ah * 0.24)
    tgt = (ox + aw * 0.80, oy - ah * 0.80)
    s.line([(cur[0], cur[1] - 30), (tgt[0], tgt[1] + 34)], color=C['green'], sw=3, dash=True)
    s.circle(*cur, 26, fill=C['brand'])
    s.text(cur[0] - 210, cur[1] - 22, 175, 44, '{b:当前：通用RN自动生成}\n快，但偏研发语言', size=13.5, color=C['text'], align='r', valign='m', lh=1.35)
    s.circle(*tgt, 30, fill=C['green'])
    s.text(tgt[0] - 225, tgt[1] - 22, 185, 44, '{b:目标：定制RN又快又好}\n提升客户满意度', size=13.5, color=C['text'], align='r', valign='m', lh=1.35)
    # 右：现状-差距-方向
    s.rect(650, 130, 570, 120, fill=C['light'], rx=10)
    s.check(680, 160, 13, C['brand'])
    s.text(702, 145, 480, 30, '现状：效率突飞猛进', size=18, color=C['brand'], bold=True, valign='m', lh=1.2)
    s.text(672, 185, 530, 56, '通用RN自动生成实践在生产效率上有突飞猛进', size=15.5, color=C['text'], lh=1.45)
    s.rect(650, 268, 570, 190, fill=C['orangel'], rx=10)
    s.text(672, 282, 480, 30, '差距：内容仍需提升', size=18, color=C['orange'], bold=True, valign='m', lh=1.2)
    gaps = [('语言风格偏研发语言', '对客户的可阅读性不够友好'), ('对定制RN的自动生成支撑度不足', '定制RN要做到又快又好，还需继续努力')]
    for i, (t, d) in enumerate(gaps):
        y = 322 + i * 64
        s.num(684, y + 22, i + 1, C['orange'], r=13, size=14)
        s.text(708, y + 4, 490, 24, t, size=16, color=C['navy'], bold=True, valign='m', lh=1.2)
        s.text(708, y + 30, 490, 24, d, size=14, color=C['sub'], valign='m', lh=1.2)
    s.rect(650, 476, 570, 194, fill=C['green'], rx=10)
    s.text(672, 492, 480, 30, '方向：聚焦内容，继续努力', size=18, color=C['white'], bold=True, valign='m', lh=1.2)
    s.text(672, 532, 530, 130, ['让RN内容更贴近客户语言，提升可读性', '增强对定制RN自动生成的支撑',
                                '定制RN做到又快又好，提升客户满意度'],
           size=16, color=C['white'], bullet='•', gap=8, lh=1.45)
    return s


# ------------------------------------------------------------------ 14 结束
def s14():
    s = Slide(bg=C['brand'])
    s.text(0, 230, W, 110, '谢谢', size=80, color=C['white'], bold=True, align='c', valign='m', lh=1.0)
    s.rect(600, 360, 80, 4, fill=C['white'])
    s.text(0, 385, W, 44, '让定制RN需求随业务而生，随系统而行', size=26, color=C['white'], align='c', valign='m', lh=1.2)
    s.text(0, 600, W, 26, 'CCN文档团队', size=16, color='#CFE9F8', align='c', valign='m', lh=1.0)
    return s


SLIDES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14]
