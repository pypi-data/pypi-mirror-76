from enum import Enum, auto

from pywood.errors import UnknownProviderError


class Provider(Enum):
    """Класс опреяющий провайдер обращения к Telegram Bot Api.


    """
    telegrambotapiwrapper = auto()  # https://github.com/pynista/telegrambotapiwrapper
    python_telegram_bot = auto()  # https://github.com/python-telegram-bot/python-telegram-bot
    pyTelegramBotAPI = auto()  # https://github.com/eternnoir/pyTelegramBotAPI


def get_provider_from_update(update) -> Provider:
    """Получить провайдера, который исользовался для получения update."""
    if hasattr(update, 'de_json'):
        return Provider.pyTelegramBotAPI
    elif hasattr(update, 'effective_user'):
        return Provider.python_telegram_bot
    elif hasattr(update, '_is_simple_type'):
        return Provider.telegrambotapiwrapper
    else:
        raise UnknownProviderError("Неизвестный провайдер.")


def get_provider_from_api_cls(cls) -> Provider:
    if hasattr(cls, ' _get_tg_api_method_name'):
        return Provider.telegrambotapiwrapper
    elif hasattr(cls, 'enable_save_reply_handlers') and \
            hasattr(cls, 'load_reply_handlers'):
        return Provider.pyTelegramBotAPI
    elif hasattr(cls, '_message') and \
            hasattr(cls, 'request') and \
            hasattr(cls, '_validate_token'):
        return Provider.python_telegram_bot
    else:
        raise UnknownProviderError("Неизвестный провайдер.")
