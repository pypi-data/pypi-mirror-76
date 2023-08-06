"""Модуль для работы с pooling."""
from typing import Callable

from requests import Timeout
from telegrambotapiwrapper import Api


def _process_existing_updates(bot_api, handler):
    offset = None

    while True:
        existing_updates = bot_api.get_updates(offset=offset)
        if existing_updates:
            for update in existing_updates:
                handler(update)
                offset = update.update_id + 1
        else:
            return


def listen(token_or_api_provider_instance,
           handler: Callable,
           process_existing: bool = False,
           ):
    """

    :param token: токен
    :type token: str

    :param handler: функция-обработчик
    :type handler: callable, принимающее один аргумент вида `update <https://core.telegram.org/bots/api#update>`_

    :param process_existing: (optional) обработать уже скопившиеся обновления
        или нет
    :type process_existing: bool

    .. Note:: Если process_existing равно False, то хотя скопившиеся
        обновления не будут обработаны обработчиком handler, но они будут
        `подтверждены <https://core.telegram.org/bots/faq#long-polling-gives-me-the-same-updates-again-and-again>`_
    """
    timeout = 20
    if type(token_or_api_provider_instance) is str:
        bot_api = Api(token=token_or_api_provider_instance)
    else:
        bot_api = token_or_api_provider_instance

    if process_existing:
        _process_existing_updates(bot_api, handler)
    else:
        _process_existing_updates(bot_api, lambda update: None)

    offset = None
    while True:
        try:
            updates = bot_api.get_updates(offset=offset, timeout=timeout)
        except Timeout:
            continue
        for update in updates:
            handler(update)
            offset = update.update_id + 1
