"""把「股市牛熊信号板」长图拆成定量、定性两张三栏图。

用法：python3 split_signal_board.py 长图.png 日期(如20261119) [输出目录]

做法：按“整行都是同一底色”识别卡片之间的间隔，切出每个小图；每块上下多留 19px 底色，
按三栏拼接，栏间留白 60px。跑完会打印识别到的小图数量和每栏高度。
如果长图里的指标数量或顺序变了，先看打印的分段结果，再改下面的 QUANT / QUAL。
"""
import os
import sys

import numpy as np
from PIL import Image

MARGIN, GAP = 19, 60
# 长图里从上到下的顺序（第 1、2 段是标题，跳过）
NAMES = ['星级', '波动', '巴菲特', '市净率', '股债',
         '融资', '成交', 'ETF', '新股', 'M2', '风格', '新发', '限购', '消息']
QUANT = [['星级', '巴菲特'], ['市净率'], ['波动', '股债']]
QUAL = [['融资', '成交', 'ETF'], ['新股', 'M2', '风格'], ['新发', '限购', '消息']]


def segments(arr):
    h = arr.shape[0]
    ref = arr[:, 8:9, :]
    gap = (np.abs(arr[:, 40:-40] - ref).sum(axis=2) < 40).mean(axis=1) > 0.98
    segs, start = [], None
    for y in range(h):
        if not gap[y] and start is None:
            start = y
        if gap[y] and start is not None:
            if y - start > 40:
                segs.append((start, y))
            start = None
    if start is not None:
        segs.append((start, h))
    return segs


def build(im, segs, cols, path):
    def column(names):
        crops = [im.crop((0, segs[n][0] - MARGIN, im.width, segs[n][1] + MARGIN)) for n in names]
        c = Image.new('RGB', (im.width, sum(x.height for x in crops)), 'white')
        y = 0
        for x in crops:
            c.paste(x, (0, y))
            y += x.height
        return c

    cs = [column(c) for c in cols]
    out = Image.new('RGB', (sum(c.width for c in cs) + GAP * (len(cs) - 1), max(c.height for c in cs)), 'white')
    x = 0
    for c in cs:
        out.paste(c, (x, 0))
        x += c.width + GAP
    out.save(path)
    print(path, out.size, [c.height for c in cs])


def main():
    src, date = sys.argv[1], sys.argv[2]
    outdir = sys.argv[3] if len(sys.argv) > 3 else '.'
    im = Image.open(src).convert('RGB')
    segs = segments(np.array(im).astype(int))
    print('识别到分段：', len(segs), segs)
    panels = segs[2:]
    if len(panels) != len(NAMES):
        sys.exit(f'小图数量 {len(panels)} 与预设 {len(NAMES)} 不符，先核对长图，再改 NAMES/QUANT/QUAL')
    named = dict(zip(NAMES, panels))
    build(im, named, QUANT, os.path.join(outdir, f'定量信号_{date}.png'))
    build(im, named, QUAL, os.path.join(outdir, f'定性信号_{date}.png'))


if __name__ == '__main__':
    main()
