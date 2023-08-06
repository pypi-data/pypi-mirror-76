from typing import Callable, List, Tuple

from ject import oneself
from palett import Preset, fluo_vector
from palett.presets import FRESH, PLANET
from texting import ELLIP
from veho.vector import mutazip
from veho.vector.length import length

from xbrief.enum.brackets import BRK
from xbrief.lines import liner
from xbrief.margin import VectorMargin


def deco_vector(
        vec: list,
        read: Callable = None,
        head: int = None,
        tail: int = None,
        presets: Tuple[Preset] = (FRESH, PLANET),
        effects: List[str] = None,
        delim=',\n',
        bracket=BRK,
        discrete=False
):
    size = length(vec)
    if not size: return str(vec)
    vn = VectorMargin.build(vec, head, tail)
    raw, text = vn.map(oneself).to_list(ELLIP), vn.stringify(read).to_list(ELLIP)
    if presets:
        dyes = fluo_vector(raw, presets, effects, colorant=True, mutate=True)
        text = mutazip(text, dyes, lambda tx, dy: dy(tx))
    return liner(text, delim=delim, bracket=bracket, discrete=discrete)
