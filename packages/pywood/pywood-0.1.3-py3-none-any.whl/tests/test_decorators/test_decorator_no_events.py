"""Module for testing the `event` decorator."""
import unittest
from unittest.mock import MagicMock

from pywood import decorators
from pywood.context import Context
from pywood.decorators import events, no_events, event
from pywood.events import BaseEvent
from pywood._exceptions import EventHandled
from pywood.states import BaseState


class EventTrue1(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return True

class EventTrue2(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return True

class EventTrue3(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return True


class EventFalse1(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return False

class EventFalse2(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return False

class EventFalse3(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return False

class EventFalse4(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return False


class TestNoEventsDecorator(unittest.TestCase):
    """Testing the `event` decorator."""

    def test_method_called_once_with(self):

        class State(BaseState):
            def handler1(self, update, event_cls, data):
                pass

            def handler2(self, update, event_cls, data):
                pass

            def handler3(self, update, data):
                pass

        handler1_mock = MagicMock(__name__='handler1')
        handler2_mock = MagicMock(__name__='handler2')
        handler3_mock = MagicMock(__name__='handler3')
        State.handler1 = events(EventFalse1, EventFalse2)(handler1_mock)
        State.handler2 = events(EventFalse3, EventFalse4)(handler2_mock)
        State.handler2 = no_events(handler3_mock)
        state = State()
        state._traverse_handlers(update='test_update',
                                 state_data={'test_data': 12345})
        handler1_mock.assert_not_called()
        handler2_mock.assert_not_called()
        handler3_mock.assert_called_once_with(
            state, 'test_update', Context(None, {'test_data': 12345}))

    def test_decorated_method_not_called(self):

        class State(BaseState):
            def handler1(self, update, data):
                pass

            def handler2(self, update, event_cls, data):
                pass

            def handler3(self, update, data):
                pass

        handler1_mock = MagicMock(__name__='handler1')
        handler2_mock = MagicMock(__name__='handler2')
        handler3_mock = MagicMock(__name__='handler2')

        State.handler1 = event(EventFalse1)(handler1_mock)
        State.handler2 = events(EventFalse2, EventTrue1)(handler2_mock)
        State.handler3 = no_events(handler3_mock)
        state = State()
        state._traverse_handlers(update='test_update',
                                 state_data={'test_data': 12345})
        handler1_mock.assert_not_called()
        handler2_mock.assert_called_once_with(state, 'test_update',
                                              Context(EventTrue1,
                                                      {'test_data': 12345}))
        handler3_mock.assert_not_called()


    def test_before_after_called(self):
        class State(BaseState):

            def handler(self, update, data):
                pass

            def before_handling(self, method_name, context):
                pass

            def after_handling(self, method_name, context):
                pass

        handler_mock = MagicMock(__name__='handler')
        after_mock = MagicMock()
        before_mock = MagicMock()
        State.handler = no_events(handler_mock)
        State.after_handling = after_mock
        State.before_handling = before_mock
        state = State()
        state._traverse_handlers(update='test_update',
                                 state_data={'test_data': 12345})
        before_mock.assert_called_once_with('handler', Context(None, {
            'test_data': 12345}))
        after_mock.assert_called_once_with('handler',
                                           Context(None, {'test_data': 12345}))

    def test_not_raises_EventHandled_exception(self):
        class State(BaseState):
            @no_events
            def handler(self, update, data):
                pass

        state = State()
        try:
            state.handler('update', 'data')
        except EventHandled:
            self.assertTrue(False)

    def test_has_attr(self):
        """Testing the presence of the `_event_handler` attribute on the decorated method."""

        class A:
            @decorators.no_events
            def foo(self, a, b, c):
                return a + b + c

            def foo1(self):
                return

        self.assertTrue(hasattr(A().foo, '_no_events'))
        self.assertFalse(hasattr(A().foo1, '_no_events'))

