from ject import oneself
from palett import fluo_matrix
from palett.presets import FRESH, PLANET
from texting import COLF, COSP, ELLIP
from veho.enum.matrix_directions import ROWWISE
from veho.matrix import size
from veho.vector import mapper

from xbrief.bracket import bracket as bracket_fn
from xbrief.enum.brackets import BRK
from xbrief.lines import liner
from xbrief.margin import MatrixMargin
from xbrief.padder.pad_matrix import pad_matrix


def deco_matrix(matrix,
                discrete=False,
                delim=COSP,
                bracket=BRK,
                read=None,
                presets=(FRESH, PLANET),
                direct=ROWWISE,
                top=0,
                bottom=0,
                left=0,
                right=0,
                ansi=False,
                level=0,
                hr=ELLIP):
    if not matrix: return str(matrix)
    height, width = size(matrix)
    if not height or not width: return liner([], delim, level, bracket, discrete)
    vn = MatrixMargin.build(matrix, top, bottom, left, right, height, width)
    raw, text = vn.map(oneself).to_matrix(hr), vn.stringify(read).to_matrix(hr)
    dye = fluo_matrix(raw, direct, presets, colorant=True) if presets else None
    rows = pad_matrix(text, raw, dye, ansi)
    lines = mapper(rows, lambda line: bracket_fn(delim.join(line))) \
        if bracket \
        else mapper(rows, lambda line: delim.join(line))
    return liner(lines, delim=COLF, bracket=bracket, level=level, discrete=discrete)
