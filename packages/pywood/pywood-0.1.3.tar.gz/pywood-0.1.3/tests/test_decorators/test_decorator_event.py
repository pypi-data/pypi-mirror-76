"""Module for testing the `event` decorator."""
import unittest
from unittest.mock import MagicMock

from pywood import decorators
from pywood.context import Context
from pywood.decorators import event
from pywood.events import BaseEvent
from pywood._exceptions import EventHandled
from pywood.states import BaseState


class EventTrue(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return True


class EventFalse(BaseEvent):
    @staticmethod
    def happened(update) -> bool:
        return False


class TestEventDecorator(unittest.TestCase):
    """Testing the `event` decorator.

    """

    def test_first_decorated_method_called_once_with(self):

        class State(BaseState):
            def handler1(self, update, context):
                pass

            def handler2(self, update, context):
                pass

        handler1_mock = MagicMock(__name__='handler1')
        handler2_mock = MagicMock(__name__='handler2')
        State.handler1 = event(EventFalse)(handler1_mock)
        State.handler2 = event(EventTrue)(handler2_mock)
        state = State()
        state._traverse_handlers(update='test_update',
                                 state_data={'test_data': 12345})
        handler1_mock.assert_not_called()
        handler2_mock.assert_called_once_with(
            state, 'test_update', Context(EventTrue, {'test_data': 12345}))

    def test_decorated_method_not_called(self):

        class State(BaseState):
            def handler1(self, update, context):
                pass

            def handler2(self, update, context):
                pass

        handler1_mock = MagicMock(__name__='handler1')
        handler2_mock = MagicMock(__name__='handler2')
        State.handler1 = event(EventFalse)(handler1_mock)
        State.handler2 = event(EventFalse)(handler2_mock)
        state = State()
        state._traverse_handlers(update='test_update',
                                 state_data={'test_data': 12345})
        handler1_mock.assert_not_called()
        handler2_mock.assert_not_called()

    def test_first_decorated_method_called_once_with_second_not_called(self):

        class State(BaseState):
            def handler1(self, update, context):
                pass

            def handler2(self, update, context):
                pass

        handler1_mock = MagicMock(__name__='handler1')
        handler2_mock = MagicMock(__name__='handler2')
        State.handler1 = event(EventTrue)(handler1_mock)
        State.handler2 = event(EventFalse)(handler2_mock)
        state = State()
        state._traverse_handlers('test_update',
                                 {'test_data': 12345})
        handler1_mock.assert_called_once_with(
            state, 'test_update', Context(EventTrue, {'test_data': 12345}))
        handler2_mock.assert_not_called()

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
        State.handler = event(EventTrue)(handler_mock)
        State.after_handling = after_mock
        State.before_handling = before_mock
        state = State()
        state._traverse_handlers(update='test_update',
                                 state_data={'test_data': 12345})
        before_mock.asssert_called_once_with('handler', Context(EventTrue, {
            'test_data': 12345}))
        after_mock.assert_called_once_with('handler', Context(EventTrue, {
            'test_data': 12345}))

    def test_raises_EventHandled_exception(self):
        class State(BaseState):
            @event(EventTrue)
            def handler(self, update, context):
                pass

        state = State()
        try:
            state.handler('update', 'context')
        except EventHandled:
            pass
        else:
            self.assertTrue(False)

    def test_not_raises_EventHandled_exception(self):
        class State(BaseState):
            @event(EventFalse)
            def handler(self, update, context):
                pass

        state = State()
        try:
            state.handler('update', 'context')
        except EventHandled:
            self.assertTrue(False)

    def test_has_attr(self):
        """Testing the presence of the `_event_handler` attribute on the decorated method."""

        class A:
            @decorators.event(MagicMock())
            def foo(self, a, b, c):
                return a + b + c

            def foo1(self):
                return

        self.assertTrue(hasattr(A().foo, '_event_handler'))
        self.assertFalse(hasattr(A().foo1, '_event_handler'))

