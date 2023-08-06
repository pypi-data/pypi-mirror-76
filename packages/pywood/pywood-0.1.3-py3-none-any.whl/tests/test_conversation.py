import unittest
from unittest.mock import Mock

from pywood._conversation import Conversation
from pywood.context import Context
from pywood.decorators import event, no_events, events
from pywood.events import BaseEvent
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



class TestConversation(unittest.TestCase):
    def test_method__get_state_from_state_name(self):
        class State1(BaseState):
            pass

        class State2(BaseState):
            pass

        class State3(BaseState):
            pass

        conversation = Conversation(state_getter=lambda update: State3,
                                    states=[State1, State2, State3])

        self.assertIs(conversation.get_state_from_state_name('State2'), State2)

    def test_method__get_current_state(self):
        class State1(BaseState):
            pass

        class State2(BaseState):
            pass

        class State3(BaseState):
            pass

        conversation = Conversation(state_getter=lambda update: State2,
                                    states=[State1, State2, State3])
        self.assertIs(conversation.get_current_state(state='State2')[0], State2)
        self.assertIs(conversation.get_current_state(state=State2)[0], State2)
    def test_method_process(self):
        state1_method1_mock = Mock()
        state1_method2_mock = Mock()
        state1_method3_mock = Mock()
        state1_method4_mock = Mock()
        state1_method5_mock = Mock()
        state1_method6_mock = Mock()

        state2_method1_mock = Mock()
        state2_method2_mock = Mock()
        state2_method3_mock = Mock()
        state2_method4_mock = Mock()
        state2_method5_mock = Mock()
        state2_method6_mock = Mock()

        state3_method1_mock = Mock()
        state3_method2_mock = Mock()
        state3_method3_mock = Mock()
        state3_method4_mock = Mock()
        state3_method5_mock = Mock()
        state3_method6_mock = Mock()

        state4_method1_mock = Mock()
        state4_method2_mock = Mock()
        state4_method3_mock = Mock()
        state4_method4_mock = Mock()
        state4_method5_mock = Mock()
        state4_method6_mock = Mock()

        before_handling_mock_state1 = Mock()
        before_handling_mock_state2 = Mock()
        before_handling_mock_state3 = Mock()
        before_handling_mock_state4 = Mock()
        after_handling_mock_state1 = Mock()
        after_handling_mock_state2 = Mock()
        after_handling_mock_state3 = Mock()
        after_handling_mock_state4 = Mock()

        class Event1(BaseEvent):
            @staticmethod
            def happened(update) -> bool:
                if update == 'event1':
                    return True
                else:
                    return False

        class Event2(BaseEvent):
            @staticmethod
            def happened(update) -> bool:
                if update == 'event2':
                    return True
                else:
                    return False

        class Event3(BaseEvent):
            @staticmethod
            def happened(update) -> bool:
                if update == 'event3':
                    return True
                else:
                    return False

        class Event4(BaseEvent):
            @staticmethod
            def happened(update) -> bool:
                if update == 'event4':
                    return True
                else:
                    return False

        class Event5(BaseEvent):
            @staticmethod
            def happened(update) -> bool:
                if update == 'event5':
                    return True
                else:
                    return False

        class Event6(BaseEvent):
            @staticmethod
            def happened(update=None) -> bool:
                if update == 'event6':
                    return True
                else:
                    return False

        class TestState1(BaseState):
            @event(Event4)
            def method1(self, update, context):
                state1_method1_mock()

            @no_events
            def method2(self, update, context):
                state1_method2_mock()

            def method3(self, update, context):
                state1_method3_mock()

            @events(Event1, Event2, Event3)
            def method4(self, update, context):
                state1_method4_mock()

            @events(Event5)
            def method5(self, update, context):
                state1_method5_mock()

            @events(Event5)
            def method6(self, update, context):
                state1_method6_mock()

            def after_handling(self, method_name, context):
                after_handling_mock_state1(method_name, context)

            def before_handling(self, method_name, context):
                before_handling_mock_state1(method_name, context)

        class TestState2(BaseState):
            @event(Event5)
            def method1(self, update, context):
                state2_method1_mock()

            @no_events
            def method2(self, update, context):
                state2_method2_mock()

            def method3(self, update, context):
                state2_method3_mock()

            @events(Event2, Event3)
            def method4(self, update, context):
                state2_method4_mock()

            @events(Event1)
            def method5(self, update, context):
                state2_method5_mock()

            def method6(self):
                state2_method6_mock()

            def after_handling(self, method_name, context):
                after_handling_mock_state2(method_name, context)

            def before_handling(self, method_name, context):
                before_handling_mock_state2(method_name, context)

        class TestState3(BaseState):
            @events(Event4, Event5, Event6)
            def method1(self, update, context):
                state3_method1_mock()

            @no_events
            def method2(self, update, context):
                state3_method2_mock()

            def method3(self, update, context):
                state3_method3_mock()

            @events(Event1, Event2, Event3)
            def method4(self, update, context):
                state3_method4_mock()

            def method5(self, update, context):
                state3_method5_mock()

            def method6(self, update, context):
                state3_method6_mock()

            def after_handling(self, method_name, context):
                after_handling_mock_state3(method_name, context)

            def before_handling(self, method_name, context):
                before_handling_mock_state3(method_name, context)

        class TestState4(BaseState):
            @event(Event5)
            def method1(self, update, context):
                state4_method1_mock()

            def method2(self, update, context):
                state4_method2_mock()

            def method3(self, update, context):
                state4_method3_mock()

            @events(Event2, Event3)
            def method4(self, update, context):
                state4_method4_mock()

            @events(Event1)
            def method5(self, update, context):
                state4_method5_mock()

            def method6(self, update, context):
                state4_method6_mock()

            def after_handling(self, method_name, context):
                after_handling_mock_state4(method_name, context)

            def before_handling(self, method_name, context):
                before_handling_mock_state4(method_name, context)

        conversation = Conversation(state_getter=lambda update: TestState1,
                                    states=[TestState1, TestState2,
                                            TestState3])
        conversation.process(update='event5',
                        state_attrs={'bla': 123, 'tiktak': 'Barack Trump'})
        state1_method1_mock.assert_not_called()
        state1_method2_mock.assert_not_called()
        state1_method3_mock.assert_not_called()
        state1_method4_mock.assert_not_called()
        state1_method5_mock.assert_called_once()
        state1_method6_mock.assert_not_called()
        before_handling_mock_state1.assert_called_once_with('method5',
                                                            Context(Event5,
                                                                    None))
        after_handling_mock_state1.assert_called_once_with('method5',
                                                           Context(Event5,
                                                                   None))

        conversation = Conversation(state_getter=lambda update: TestState2,
                                    states=[TestState1, TestState2,
                                            TestState3])
        conversation.process(update='event6')
        state2_method1_mock.assert_not_called()
        state2_method2_mock.assert_called_once()
        state2_method3_mock.assert_not_called()
        state2_method4_mock.assert_not_called()
        state2_method5_mock.assert_not_called()
        state2_method6_mock.assert_not_called()
        before_handling_mock_state2.assert_called_once_with('method2',
                                                            Context(None,
                                                                    None))
        after_handling_mock_state2.assert_called_once_with('method2',
                                                           Context(None, None))

        conversation = Conversation(state_getter=lambda update: TestState3,
                                    states=[TestState1, TestState2,
                                            TestState3])
        conversation.process(update='event5')
        state3_method1_mock.assert_called_once()
        state3_method2_mock.assert_not_called()
        state3_method3_mock.assert_not_called()
        state3_method4_mock.assert_not_called()
        state3_method5_mock.assert_not_called()
        state3_method6_mock.assert_not_called()
        before_handling_mock_state3.assert_called_once_with('method1',
                                                            Context(Event5,
                                                                    None))
        after_handling_mock_state3.assert_called_once_with('method1',
                                                           Context(Event5,
                                                                   None))

        conversation = Conversation(state_getter=lambda update: TestState4,
                                    states=[TestState1, TestState2,
                                            TestState3])
        conversation.process(update='event6')
        state4_method1_mock.assert_not_called()
        state4_method2_mock.assert_not_called()
        state4_method3_mock.assert_not_called()
        state4_method4_mock.assert_not_called()
        state4_method5_mock.assert_not_called()
        state4_method6_mock.assert_not_called()
        before_handling_mock_state4.assert_not_called()
        after_handling_mock_state4.assert_not_called()

    def test_state_has_passed_from_handle_update_attrs(self):
        class State1(BaseState):
            pass

        class State2(BaseState):
            pass

        class State3(BaseState):
            def _traverse_handlers(self2, *args, **kwargs):
                self.assertTrue(self2.db_conn == 'db_connection')
                self.assertTrue(self2.bot_api == 'bot_api')

        class State4(BaseState):
            pass

        conversation = Conversation(state_getter=lambda update: State3,
                                    states=[State1, State2, State3, State4])
        conversation.process(update=Mock(),
                        state_attrs={
                            'db_conn': 'db_connection',
                            'bot_api': 'bot_api',
                        }
                        )