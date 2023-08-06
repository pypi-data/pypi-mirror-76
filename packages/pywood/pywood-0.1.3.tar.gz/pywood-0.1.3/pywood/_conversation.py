"""Класс определяющий основную функциональность."""
from __future__ import annotations

from typing import List, Type, Callable, TypeVar, Tuple, Any

from pywood.errors import StateDoesNotExistError
from pywood.states import BaseState

Update = TypeVar('Update')


class Conversation:
    """Класс определяющий работу с состояниями."""

    def __init__(self,
                 *,
                 state_getter: Callable,
                 states: List[Type[BaseState]]):
        """Проинициализировать класс определяющий работу с состояниями.

        :param state_getter: функция, принимающая Update и \
        возвращающая либо строку, которая является названием текущего \
        состояния, либо сам класс текущего состояния
        :type state_getter: функция

        :param states: список состояний чата
        :type states: список из классов унаследованных от State
        """
        self.state_getter = state_getter
        self.states = states

    def get_state_from_state_name(self, state_name: str) -> Type[BaseState]:
        """Получить класс состояния из названия класса состояния."""
        for state in self.states:
            if state.__name__ == state_name:
                return state
        raise StateDoesNotExistError

    def get_current_state(self, state) -> Tuple[Type[BaseState], Any]:
        """Получить текущее состояние"""
        if isinstance(state, str):
            return self.get_state_from_state_name(state), None
        elif isinstance(state, tuple):
            if isinstance(state[0], str):
                return self.get_state_from_state_name(state[0]), state[1]
            elif issubclass(state[0], BaseState):
                return state[0], state[1]
            else:
                raise StateDoesNotExistError

        elif issubclass(state, BaseState):
            return state, None
        else:
            raise StateDoesNotExistError(
                "`state_getter` должна возвращать"
                " строку, класс или кортеж вида (str, Any)")

    @staticmethod
    def add_attrs(obj, attrs):
        for key, value in attrs.items():
            setattr(obj, key, value)

    def process(self,
                update: Update,
                state_attrs=None,
                ):
        """Обработать объект типа Update."""
        raw_curr_state = self.state_getter(update)
        state_cls, state_data = self.get_current_state(raw_curr_state)
        state = state_cls()
        if state_attrs:
            Conversation.add_attrs(state, state_attrs)
        state._traverse_handlers(update, state_data)
