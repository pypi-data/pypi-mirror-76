from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram_mvc.config import dp
from .base import abstractmethod, BaseMetaView, BaseView


class MetaMessageView(BaseMetaView):
    register_func = dp.register_message_handler

    @abstractmethod
    def _validator(cls, *args, **kwargs):
        pass


class MessageView(BaseView, metaclass=MetaMessageView):

    @staticmethod
    def _get_state(update_object: types.Message):
        return dp.current_state(update_object.from_user.id)

    @classmethod
    async def validate(cls, message: types.Message, state: FSMContext = None, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def main(cls, message: types.Message, validated_data: dict, state: FSMContext):
        pass
