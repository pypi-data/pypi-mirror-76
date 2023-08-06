class Error(Exception):
    """Базовый класс для ошибок `pywood`."""


class StateDoesNotExistError(Error):
    """Такое состояние не существует."""


class UnknownProviderError(Error):
    """Неизвестный провайдер."""
