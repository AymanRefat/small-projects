from typing import Any


def validate_type(value: Any, t) -> Any:
    if isinstance(value, t):
        return value
    # Try cast
    try:
        return t(value)
    except:
        raise TypeError(f"Worked Date should be a {t}")


def validate_in_list(value: Any, l: list) -> Any:
    if value in l:
        return value
    else:
        raise ValueError(f"the Gender Should be in {l}")
