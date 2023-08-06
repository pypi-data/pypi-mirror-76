from aiogram import types

from aiogram_mvc.config import dp
from .base import abstractmethod, BaseMetaView, BaseView


class MetaMessageView(BaseMetaView):
    register_func = dp.register_message_handler

    @abstractmethod
    def _validator(cls, *args, **kwargs):
        pass


class MessageView(BaseView, metaclass=MetaMessageView):

    @classmethod
    async def validate(cls, message: types.Message):
        pass

    @classmethod
    @abstractmethod
    async def main(cls, message: types.Message, validated_data: dict):
        pass
