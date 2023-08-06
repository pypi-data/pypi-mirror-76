import unittest
from unittest.mock import MagicMock, patch

from pywood.context import Context
from pywood.decorators import event, events, no_events
from pywood.events import BaseEvent
from pywood.states import BaseState

class Event1(BaseEvent):
    @staticmethod
    def happened(update=None) -> bool:
        return True


class Event2(BaseEvent):
    @staticmethod
    def happened(update=None) -> bool:
        return False


class Event3(BaseEvent):
    @staticmethod
    def happened(update=None) -> bool:
        return True


class Event4(BaseEvent):
    @staticmethod
    def happened(update=None) -> bool:
        return False


class Event5(BaseEvent):
    @staticmethod
    def happened(update=None) -> bool:
        return False


class Event6(BaseEvent):
    @staticmethod
    def happened(update=None) -> bool:
        return True


class TestState1(BaseState):
    @event(Event4)
    def method1(self, update, context):
        raise NotImplementedError

    @no_events
    def method2(self, update, context):
        raise NotImplementedError

    def method3(self, update, context):
        raise NotImplementedError

    @events(Event1, Event2, Event3)
    def method4(self, update, context):
        raise NotImplementedError

    @events(Event5)
    def method5(self, update, context):
        raise NotImplementedError

    @events(Event5)
    def method6(self, update, context):
        raise NotImplementedError


class TestStateMethods(unittest.TestCase):
    def test_method__handlers(self):
        state = TestState1()
        self.assertListEqual([method[0] for method in state._handlers()],
                             ['method1', 'method4', 'method5', 'method6']
                             )

    def test_method__no_event_handler(self):
        state = TestState1()
        self.assertEqual(state._no_event_handler()[0], 'method2')

    @patch.object(Event1, 'happened', return_value=False)
    @patch.object(Event2, 'happened', return_value=False)
    @patch.object(Event3, 'happened', return_value=False)
    @patch.object(Event4, 'happened', return_value=False)
    @patch.object(Event5, 'happened', return_value=False)
    @patch.object(Event6, 'happened', return_value=False)
    def test__traverse_handlers_called_no_events_handler(self, *args):
        method2_mock = MagicMock(__name__='method2')

        with patch.object(TestState1, 'method2', no_events(method2_mock)):
            state = TestState1()
            state._traverse_handlers('update', 'state_data')
            method2_mock.assert_called_once_with(state, 'update',
                                                 Context(None, 'state_data'))

    def test__traverse_handlers_called_first_handler(self):
        method4_mock = MagicMock(__name__='method4')

        with patch.object(TestState1, 'method4',
                          events(Event1, Event2, Event3)(method4_mock)):
            state = TestState1()
            state._traverse_handlers('update', 'state_data')
            method4_mock.assert_called_once_with(state, 'update',
                                                 Context(Event1, 'state_data'))

    def test_raises(self):
        class State(BaseState):
            def handler(self, update, context):
                pass

        state = State()
        state._traverse_handlers('update', 'state_data')

    def test_inst_classname(self):
        class MyCustomState(BaseState):
            pass

        state = MyCustomState()
        self.assertEqual(state.inst_classname, 'MyCustomState')


    def test_classname(self):
        class MyCustomState(BaseState):
            pass
        self.assertEqual(MyCustomState.classname(), 'MyCustomState')




