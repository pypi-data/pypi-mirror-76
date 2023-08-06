from functools import partial
from typing import Optional, Dict, Any, Callable, List, Type

import telegrambotapiwrapper

from pywood._conversation import Conversation
from pywood.pooling import listen
from pywood.states import BaseState


class Bot:

    def __init__(self,
                 token: str,
                 states: List,
                 state_getter: Callable,
                 api_provider_cls=telegrambotapiwrapper.Api,
                 api_provider_cls_kwargs: Optional[dict] = None,
                 state_attrs: Optional[dict] = None,
                 ):
        self.token = token
        self.states = states
        self.getter = state_getter
        self.api_provider_cls = api_provider_cls
        self.api_provider_cls_kwargs = api_provider_cls_kwargs
        self.state_attrs = state_attrs

    def start_polling(self, process_existing=False):
        if self.api_provider_cls_kwargs:
            bot_api = self.api_provider_cls(
                token=self.token,
                **self.api_provider_cls_kwargs)
        else:
            bot_api = self.api_provider_cls(self.token)
        if self.state_attrs is not None:
            state_attrs_copy = self.state_attrs.copy()
            state_attrs_copy['bot_api'] = bot_api
            handler = partial(handle_update,
                              states=self.states,
                              state_getter=self.getter,
                              state_attrs=state_attrs_copy)
        else:
            handler = partial(handle_update,
                              states=self.states,
                              state_getter=self.getter,
                              state_attrs={'bot_api': bot_api})

        listen(self.token,
               handler,
               process_existing=process_existing)

    def handle_update(self, update):
        """Обработать обновление.


        .. note::
            метод `handle_update()` добавляет аттрибут `bot_api` к объекту класса состояния
        """
        if self.api_provider_cls_kwargs:
            bot_api = self.api_provider_cls(
                token=self.token,
                **self.api_provider_cls_kwargs)
        else:
            bot_api = self.api_provider_cls(self.token)

        if self.state_attrs is not None:
            state_attrs_copy = self.state_attrs.copy()
            state_attrs_copy['bot_api'] = bot_api
            state_attrs_copy['token'] = self.token
            handle_update(update,
                          self.states,
                          self.getter,
                          state_attrs_copy)
        else:
            handle_update(update,
                          self.states,
                          self.getter,
                          {'bot_api': bot_api, 'token': self.token})


def handle_update(update,
                  states: List[Type[BaseState]],
                  state_getter: Callable,
                  state_attrs: Optional[Dict[str, Any]] = None,
                  ):
    """

    :param update: обновление
    :type update: объект, определяющий объект `Update <https://core.telegram.org/bots/api#update>`_

    :param states: список классов состояний
    :type states: список классов, наследующих от BaseState (List[Type[BaseState]])

    :param state_getter: callable, принимающее как аргумент `update`,
        и возвращающее

        - строку, содержащую название класса текущего состояния
        - сам класс текущего состояния
        - кортеж, содержащий первым своим элементом название класса текущего
          состояния и вторым элементом дополнительную информацию, которая будет
          добавлена в аргумент `context` обработчиков

    :type state_getter: callable

    :param state_attrs: (optional) словарь, содержащий аттрибуты, которые будут
        добавлены к экземпляру класса состояния
    :type state_attrs: Dict[str, Any]

    :raises StateDoesNotExistError: выбрасывается, если state_getter
        возвращает не строку, класс состояния или кортеж

    :return:

    .. warning::
        В отличие от обработки обновлений методами `start_pooling()` и `handle_update()`
        класса `Bot`, функция `handle_update()` не добавляет аттрибут `bot_api` к объекту класса состояния
    """
    conversation = Conversation(
        state_getter=state_getter,
        states=states)
    conversation.process(update=update, state_attrs=state_attrs)
