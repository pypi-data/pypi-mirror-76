"""Модуль для работы с событиями."""
from abc import ABCMeta, abstractmethod


class BaseEvent(metaclass=ABCMeta):
    """The base class for all events.

    Create custom events by inheriting from it.
    """

    @staticmethod
    @abstractmethod
    def happened(update) -> bool:
        """Проверить, сработало ли событие для данного `update`."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        """Получить имя класса события.

        :returns: имя класса события, например `IncomingText`
        :rtype: str
        """
        return self.__class__.__name__

    def __repr__(self):
        """Получить представление класса события как имя класса.

        :returns: имя класса события со скобками, например `IncomingText()`
        :rtype: str
        """
        return f'{self.__class__.__name__}()'
