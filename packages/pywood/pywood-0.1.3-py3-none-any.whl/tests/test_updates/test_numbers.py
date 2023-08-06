import unittest

from pywood.updates.numbers import is_int_number


class TestIsIntNumber(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        class Update:
            def __init__(self, message, value1, value2):
                self.message = message
                self.value1 = value1
                self.value2 = value2

        class Message:
            def __init__(self, text, value1, value2):
                self.text = text
                self.value1 = value1
                self.value2 = value2

        cls.Update = Update
        cls.Message = Message

    def test_is_int_number_assert_true(self):
        message_with_text_with_int_1 = self.Message('123', None, 23432)
        message_with_text_with_int_2 = self.Message('234', None, None)
        message_with_text_with_int_3 = self.Message('-3456', 'van', 'rossum')
        message_with_text_with_int_4 = self.Message('0', 'van', 'rossum')

        update_with_msg_with_text_with_int_1 = self.Update(message_with_text_with_int_1,
                                                           'typing',
                                                           123)

        update_with_msg_with_text_with_int_2 = self.Update(message_with_text_with_int_2,
                                                           None,
                                                           123)

        update_with_msg_with_text_with_int_3 = self.Update(message_with_text_with_int_3,
                                                           None,
                                                           'van')

        update_with_msg_with_text_with_int_4 = self.Update(message_with_text_with_int_4,
                                                           100000,
                                                           -345678)

        self.assertTrue(is_int_number(update_with_msg_with_text_with_int_1))
        self.assertTrue(is_int_number(update_with_msg_with_text_with_int_2))
        self.assertTrue(is_int_number(update_with_msg_with_text_with_int_3))
        self.assertTrue(is_int_number(update_with_msg_with_text_with_int_4))

    def test_is_int_number_assert_false(self):
        message_with_text_wo_int_1 = self.Message('123.123', None, 23432)
        message_with_text_wo_int_2 = self.Message('234234324.3423', None, None)
        message_with_text_wo_int_3 = self.Message('Elon Musk', 'van', 'rossum')
        message_with_text_wo_int_4 = self.Message('-123123.00001', 'van', 'rossum')

        message_wo_text_1 = self.Message(None, None, None)
        message_wo_text_2 = self.Message(None, 'germany', None)
        message_wo_text_3 = self.Message(None, 'belarus', 'dzmitry')

        update_with_msg_wo_text1 = self.Update(message_wo_text_1,
                                               'rossum',
                                               123)

        update_with_msg_wo_text2 = self.Update(message_wo_text_2,
                                               None,
                                               123)

        update_with_msg_wo_text3 = self.Update(message_wo_text_3,
                                               None,
                                               'guido')

        update_with_msg_wo_int_1 = self.Update(message_with_text_wo_int_1,
                                               'Jeff',
                                               'guido')

        update_with_msg_wo_int_2 = self.Update(message_with_text_wo_int_2,
                                               'Bezos',
                                               'van')

        update_with_msg_wo_int_3 = self.Update(message_with_text_wo_int_3,
                                               'Me',
                                               'rossum')

        update_with_msg_wo_int_4 = self.Update(message_with_text_wo_int_3,
                                               'Dzmitry',
                                               'Maliuzhenets')

        update_wo_msg_1 = self.Update(None, None, None)
        update_wo_msg_2 = self.Update(None, "elon", 123)
        update_wo_msg_3 = self.Update(None, "elon", "musk")

        self.assertFalse(is_int_number(update_wo_msg_1))
        self.assertFalse(is_int_number(update_wo_msg_3))
        self.assertFalse(is_int_number(update_wo_msg_2))
        self.assertFalse(is_int_number(update_with_msg_wo_text2))
        self.assertFalse(is_int_number(update_with_msg_wo_text3))
        self.assertFalse(is_int_number(update_with_msg_wo_int_1))
        self.assertFalse(is_int_number(update_with_msg_wo_int_2))
        self.assertFalse(is_int_number(update_with_msg_wo_int_3))
        self.assertFalse(is_int_number(update_with_msg_wo_int_4))
