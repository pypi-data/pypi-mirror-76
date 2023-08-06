"""Модуль для работы с состояниями."""
import inspect
from abc import ABCMeta
from typing import List, Callable, Tuple, Any

from pywood._exceptions import EventHandled


class BaseState(metaclass=ABCMeta):
    """The base class for all states.

    Create custom states by inheriting from it.
    """

    bot_api: Any

    @property
    def inst_classname(self) -> str:
        return self.__class__.__name__

    @classmethod
    def classname(cls) -> str:
        return cls.__name__

    def _handlers(self) -> List[Tuple[str, Callable]]:
        """Получить методы которые декорированы декораторами event и events."""

        def predicate(value) -> bool:
            return inspect.ismethod(value) and hasattr(value, '_event_handler')

        return inspect.getmembers(self, predicate=predicate)

    def _no_event_handler(self) -> Tuple[str, Callable]:
        """Получить метод, который декорирован декоратором no_events"""

        def predicate(value):
            return inspect.ismethod(value) and hasattr(value, '_no_events')

        return inspect.getmembers(self, predicate=predicate)[0]

    def after_handling(self, method_name, context):
        """Метод, который выполняется после обработки события.

        :param method_name: имя метода
        :type method_name: str

        :param event_cls: класс события
        :type event_cls: класс
        """
        pass

    def before_handling(self, method_name, context):
        """Метод, который выполняется перед обработкой события.

        :param method_name: имя метода
        :type method_name: str

        :param event_cls: класс события
        :type event_cls: класс
        """
        pass

    def _traverse_handlers(self, update, state_data):
        """Пройти через обработчики."""

        for method_name, method in self._handlers():
            try:
                method(update, state_data)
            except EventHandled:
                return
        else:
            try:
                method_name, method = self._no_event_handler()
            except IndexError:
                pass
            else:
                method(update, state_data)
