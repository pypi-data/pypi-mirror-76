def pad_start(text: str, width: int, fill_char: str = ' '):
    return f'{text:{fill_char[0]}>{width}}'


def pad_end(text: str, width: int, fill_char: str = ' '):
    return f'{text:{fill_char[0]}<{width}}'


def pad_centered(text: str, width: int, fill_char: str = ' '):
    return f'{text:{fill_char[0]}^{width}}'
