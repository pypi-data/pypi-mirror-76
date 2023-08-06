"""Различные утилиты."""


def delete_nones(d: dict) -> dict:
    """Удалить рекурсивно элементы с None значениями.

    :param d: словарь в котором требуется рекурсивно удалить все элементы со
    значениями None
    :type d: dict
    """
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (delete_nones(v) for v in d) if v]
    return {k: v for k, v in ((k, delete_nones(v)) for k, v in d.items()) if v}


def full_qual_class_name(cls) -> str:
    """Получить полный путь класса.

    :param cls: класс, для которого необходимо получить полный путь
    :type cls: класс
    """
    return ".".join([cls.__module__, cls.__name__])
