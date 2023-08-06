import datetime
from dataclasses import asdict

from prettyprinter import prettyprinter

from pywood._utils import delete_nones
from pywood.pooling import listen


def print_incoming_updates(token: str,
                           print_existing: bool = False,
                           print_with_nones: bool = True):
    """Слушать и печатать входящие обновления.

    :param token: токен
    :type token: str

    :param print_existing: (optional) распечатать уже скопившиеся updates
    :type print_existing: bool

    :param delay: (optional) задержка в секундах между обращениями к Telegram Bot Api
    :type delay: int

    :param print_with_nones: (optional) включать поля, которые отсутствут в полученных объектах
    :type print_with_nones: bool
    """

    def w_nones(update):
        now = datetime.datetime.now()
        print('---------{}---------'.format(now.strftime("%Y-%m-%d %H:%M:%S")))
        prettyprinter.pprint(asdict(update))

    def wo_nones(update):
        now = datetime.datetime.now()
        print('---------{}---------'.format(now.strftime("%Y-%m-%d %H:%M:%S")))
        prettyprinter.pprint(delete_nones(asdict(update)))

    handler = w_nones if print_with_nones else wo_nones
    listen(token, handler, print_existing)
