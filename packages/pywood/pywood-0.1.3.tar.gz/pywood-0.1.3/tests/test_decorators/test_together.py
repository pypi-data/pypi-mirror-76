import unittest
from unittest.mock import Mock

from pywood import BaseState
from pywood.context import Context
from pywood.decorators import event, events, no_events
from pywood.events import BaseEvent


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

class TestEventDecorator(unittest.TestCase):
    def test_no_events_called(self):
        mock1 = Mock()
        mock2 = Mock()
        mock3 = Mock()
        mock4 = Mock()

        class State(BaseState):
            @event(EventFalse1)
            def handle1(self, update, context):
                mock1(self, update, context)

            @event(EventFalse2)
            def handle2(self, update, context):
                mock2(self, update, context)

            @events(EventFalse3, EventFalse4)
            def handle3(self, update, context):
                mock3(self, update, context)

            @no_events
            def handle4(self, update, context):
                mock4(self, update, context)

        state = State()
        state._traverse_handlers('update', 'data')
        mock1.assert_not_called()
        mock2.assert_not_called()
        mock3.assert_not_called()
        mock4.assert_called_once_with(state, 'update', Context(None, 'data'))

    def test_events_called(self):
        mock1 = Mock()
        mock2 = Mock()
        mock3 = Mock()
        mock4 = Mock()

        class State(BaseState):
            @event(EventFalse1)
            def handle1(self, update, context):
                mock1(self, update, context)

            @event(EventFalse2)
            def handle2(self, update, context):
                mock2(self, update, context)

            @events(EventFalse3, EventTrue1)
            def handle3(self, update, context):
                mock3(self, update, context)

            @no_events
            def handle4(self, update, context):
                mock4(self, update, context)

        state = State()
        state._traverse_handlers('update', 'data')
        mock1.assert_not_called()
        mock2.assert_not_called()
        mock3.assert_called_once_with(state, 'update',
                                      Context(EventTrue1, 'data'))
        mock4.assert_not_called()


    def test_event_called(self):
        mock1 = Mock()
        mock2 = Mock()
        mock3 = Mock()
        mock4 = Mock()

        class State(BaseState):
            @event(EventFalse1)
            def handle1(self, update, context):
                mock1(self, update, context)

            @event(EventTrue1)
            def handle2(self, update, context):
                mock2(self, update, context)

            @events(EventFalse3, EventTrue1)
            def handle3(self, update, context):
                mock3(self, update, context)

            @no_events
            def handle4(self, update, data):
                mock4(self, update, data)

        state = State()
        state._traverse_handlers('update', state_data='data')
        mock1.assert_not_called()
        mock2.assert_called_once_with(state, 'update',
                                      Context(EventTrue1, 'data'))
        mock3.assert_not_called()
        mock4.assert_not_called()

