deleted_symbols = {
    'X': '✖️',
    'O': '🔘'
}

symbols = {
    'X': '❌',
    'O': '🔵'
}


def get_marker(value: int | str, deleted: bool = False) -> str:
    if isinstance(value, int):
        return '      '
    if deleted:
        return deleted_symbols[value]
    return symbols[value]
