import re

int_regexp = re.compile(r"[-+]?\d+$")


def _is_int(s):
    return int_regexp.match(s) is not None


def is_int_number(update) -> bool:
    try:
        text = update.message.text.strip()
    except (AttributeError, ValueError, TypeError):
        return False
    else:
        return _is_int(text)
