from aryth.bound_vector import max_by
from texting import SP, lange
from veho.columns import mapper
from veho.matrix.enumerate import duozipper, trizipper

from xbrief.padder.pad_string import to_pad


def pad_matrix(text, raw=None, dye=None, ansi=False, fill=SP):
    raw = raw if raw is not None else text
    pad = to_pad(ansi=ansi, fill=fill)
    length = lange if ansi else len
    wds = mapper(text, lambda col: max_by(col, indicator=length))
    return trizipper(text, raw, dye, lambda tx, va, dy, i, j: dy(pad(tx, wds[j], va))) \
        if dye \
        else duozipper(text, raw, lambda tx, va, i, j: pad(tx, wds[j], va))
