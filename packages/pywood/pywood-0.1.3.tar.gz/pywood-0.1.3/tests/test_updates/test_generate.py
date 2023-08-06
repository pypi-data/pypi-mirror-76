import unittest
from pywood.updates.generate import update_w_random_command
from pywood.updates.generate import update_w_random_int_number
from pywood.updates.generate import update_w_random_update_text
from pywood.updates.texts import is_msg_w_text_to_bot
from pywood.updates.commands import is_command
from pywood.updates.numbers import is_int_number
from pywood.updates.generate import get_random_update


class Test(unittest.TestCase):
    def test_update_w_random_int_number(self):
        self.assertTrue(is_int_number(update_w_random_int_number(123123123)))

    def test_update_w_random_update_text(self):
        self.assertTrue(is_msg_w_text_to_bot(update_w_random_update_text(123123123)))

    def test_update_w_random_command(self):
        self.assertTrue(is_command(update_w_random_command(123123123)))


class TestGetRandomUpdate(unittest.TestCase):

    def test_chat_ids(self):
        chat_ids_for_exclude = []
        chat_id_range = (-1000, 1000)
        for i in range(chat_id_range[0], chat_id_range[1], 4):
            chat_ids_for_exclude.append(i)
        for _ in range(1000):
            update = get_random_update(exclude_chat_ids=chat_ids_for_exclude,
                                       chat_id_range=chat_id_range)
            chat_id = update.message.chat.id
            self.assertNotIn(chat_id, chat_ids_for_exclude)


