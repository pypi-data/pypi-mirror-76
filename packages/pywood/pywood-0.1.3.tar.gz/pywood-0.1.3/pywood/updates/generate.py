import random
import string
from typing import Optional, List, Callable

"""Модуль для генерации объектов Update для целей тестирования."""


class Message:
    def __init__(self, chat, text, entities=None):
        self.chat = chat
        self.text = text
        self.entities = entities


class Chat:
    def __init__(self, id):
        self.id = id


class Update:
    def __init__(self, message):
        self.message = message


def update_w_random_int_number(chat_id):
    chat = Chat(chat_id)
    random_int = random.randint(-1000000, 1000000)
    message = Message(chat, str(random_int))
    return Update(message=message)


def update_w_random_update_text(chat_id):
    def random_string(string_length=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))

    chat = Chat(chat_id)
    message = Message(chat, random_string(50))
    return Update(message=message)


def update_w_random_command(chat_id):
    class MessageEntity:
        def __init__(self, type):
            self.type = type

    def random_string(string_length=20):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return '/' + ''.join(
            random.choice(letters) for i in range(string_length))

    chat = Chat(chat_id)
    message = Message(chat, random_string(50),
                      entities=[MessageEntity(type='bot_command')])
    return Update(message=message)


def get_random_update(exclude_chat_ids: Optional[List[int]] = None,
                      funcs: Optional[List[Callable]] = None,
                      chat_id_range=(-999999999999, 999999999999)) -> Update:
    """Сгенерировать случайное Update.

    :param exclude_chat_ids: (optional) список chat_id, которые нельзя использовать для генерации
    :type exclude_chat_ids: List[int]

    :param funcs:  (optional) список функций, которые будут участвовать в генерации объекта Update; функции должны
    принимать аргументом chat_id и возвращать объект Update
    :type funcs: List[Callable]

    :param chat_id_range: (optional) диапазон генерируемых chat_id
    :type chat_id_range: Tuple[int, int]
    """

    if not funcs:
        funcs = [
            update_w_random_int_number,
            update_w_random_update_text,
            update_w_random_command,
        ]

    func = random.choice(funcs)
    while True:
        rand_chat_id = random.randint(chat_id_range[0],
                                      chat_id_range[1])
        if exclude_chat_ids:
            if rand_chat_id in exclude_chat_ids:
                continue
            else:
                return func(rand_chat_id)
        else:
            return func(rand_chat_id)
