"""Модуль для работы с декораторами."""
import logging
from functools import wraps
from typing import Type

from pywood._exceptions import EventHandled
from pywood.context import Context
from pywood.events import BaseEvent

logger = logging.getLogger(__name__)


def event(event_cls: Type[BaseEvent]):
    """Декоратор для определения одного обрабатываемого события.

    :param event_cls: класс, определяющий событие, которое должен обработать \
    декорируемый метод
    :type event_cls: Type[BaseEvent]

    .. note:: blabla kjhkhjkhkjhkhkjhjkhjk
    """

    def decorator(method):
        method.__dict__['_event_handler'] = True

        @wraps(method)
        def wrapper(state, update, state_data):
            method_name = method.__name__
            if event_cls.happened(update):
                context = Context(event_cls, state_data)

                state.before_handling(method_name, context)
                method(state, update, context)
                state.after_handling(method_name, context)
                raise EventHandled

        return wrapper

    return decorator


def events(*event_classes):
    """Декоратор для определения нескольких обрабатываемых событий.

    :param event_classes: классы событий
    :type event_classes: классы событий в виде позиционных аргументов

    :param pass_event_cls: передавать ли в функцию обработчик событие. Функция\
     должна принимать данный аргумент.
    :type pass_event_cls: bool
    """

    def decorator(method):
        method.__dict__['_event_handler'] = True
        method_name = method.__name__

        @wraps(method)
        def wrapper(state, update, state_data):
            for event_cls in event_classes:
                if event_cls.happened(update):
                    context = Context(event_cls, state_data)

                    state.before_handling(method_name, context)
                    method(state, update, context)
                    state.after_handling(method_name, context)

                    raise EventHandled

        return wrapper

    return decorator


def no_events(method):
    """Декоратор для метода срабатывающего если не обрабатывались события."""
    method.__dict__['_no_events'] = True
    method_name = method.__name__

    @wraps(method)
    def wrapper(state, update, state_data):
        context = Context(None, state_data)
        state.before_handling(method_name, context)
        method(state, update, context)

        state.after_handling(method_name, context)

    return wrapper
