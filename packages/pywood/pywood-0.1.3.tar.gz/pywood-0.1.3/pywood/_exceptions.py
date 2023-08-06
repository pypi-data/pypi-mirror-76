"""Исключения."""


class AppExc(Exception):
    """Базовый класс для исключений связанных с пакетом."""


class EventHandled(AppExc):
    """Событие обработано."""
