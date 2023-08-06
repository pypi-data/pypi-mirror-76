from aryth.bound_entries import max_by
from texting import SP, lange
from veho.entries import duozipper, trizipper

from xbrief.padder.pad_string import to_lpad, to_pad


def pad_entries(text, raw=None, dye=None, ansi=False, fill=SP):
    raw = raw if raw is not None else text
    lpad, pad = to_lpad(ansi=ansi, fill=fill), to_pad(ansi=ansi, fill=fill)
    kw, vw = max_by(text, lange if ansi else len)
    return trizipper(
        text, raw, dye,
        lambda tx, va, dy: dy(lpad(tx, kw)),
        lambda tx, va, dy: dy(pad(tx, vw, va))
    ) \
        if dye \
        else duozipper(
        text, raw,
        lambda tx, va: lpad(tx, kw),
        lambda tx, va: pad(tx, vw, va)
    )
