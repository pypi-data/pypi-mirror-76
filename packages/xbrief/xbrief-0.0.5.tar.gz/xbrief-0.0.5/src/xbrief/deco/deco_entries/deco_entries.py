from typing import Callable, List, Tuple

from ject import oneself
from palett import Preset, fluo_entries
from palett.presets import FRESH, PLANET
from texting import ELLIP, LF
from veho.entries import zipper
from veho.vector import mapper
from veho.vector.length import length

from xbrief.bracket import to_br
from xbrief.enum.brackets import BRK
from xbrief.lines import liner
from xbrief.margin import EntriesMargin
from xbrief.padder.pad_entries import pad_entries


def deco_entries(
        vec: list,
        key_read: Callable = None,
        read: Callable = None,
        head: int = None,
        tail: int = None,
        presets: Tuple[Preset] = (FRESH, PLANET),
        effects: List[str] = None,
        delim: str = ',\n',
        bracket: int = BRK,
        ansi: bool = False,
        dash: str = ': '
):
    size = length(vec)
    if not size: return str(vec)
    vn = EntriesMargin.build(vec, head, tail)
    raw, text = vn.to_list(ELLIP), vn.stringify(key_read, read).to_list(ELLIP)
    dye = fluo_entries(raw, presets, effects, colorant=True, mutate=True) if presets else None
    entries = pad_entries(text, raw, dye, ansi=presets or ansi) \
        if delim.find(LF) >= 0 \
        else zipper(text, dye, lambda tx, dy: dy(tx)) if presets else text
    brk = to_br(bracket) or oneself
    lines = mapper(entries, lambda entry: brk(entry[0] + dash + entry[1].rstrip()))
    return liner(lines, delim=delim, bracket=bracket)
