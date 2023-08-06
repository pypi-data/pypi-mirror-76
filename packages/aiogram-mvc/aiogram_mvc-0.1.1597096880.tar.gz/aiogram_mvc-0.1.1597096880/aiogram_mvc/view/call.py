from abc import ABC

from aiogram import types
from mdocument import DocumentDoesntExist

from aiogram_mvc.config import dp
from aiogram_mvc.middleware.callback import GetCallDataMiddleware
from aiogram_mvc.middleware.middleware import MiddlewareList
from aiogram_mvc.model.call_data import CallbackData
from aiogram_mvc.view.base import abstractmethod, BaseMetaView, BaseView


class MetaCallbackView(BaseMetaView, ABC):
    register_func = dp.register_callback_query_handler

    def __init__(cls, *args, **kwargs):
        super(BaseMetaView, cls).__init__(*args, **kwargs)
        if cls.__module__ != __name__:
            if getattr(cls, "handler_kwargs", None) is None:
                raise Exception(f"handler_kwargs is required in {cls}")
            cls.register_func(cls._validator(cls.main),
                              *[cls.call_match],
                              **cls.handler_kwargs)

    async def call_match(cls, call):
        try:
            await CallbackData.one(view_cls_id=cls.id, call_id=call.data)
            return True
        except DocumentDoesntExist:
            return False


class CallbackView(BaseView, metaclass=MetaCallbackView):
    middleware = MiddlewareList(GetCallDataMiddleware)

    @staticmethod
    async def _get_state(update_object: types.CallbackQuery):
        return dp.current_state(update_object.from_user.id)

    @classmethod
    async def validate(cls, call: types.CallbackQuery, call_data: CallbackData, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def main(cls, call: types.CallbackQuery,
                   validated_data: dict,
                   call_data: CallbackData,
                   state: "FSMContext"):
        pass

    @classmethod
    async def generate_callback(cls, data: dict):
        return (await CallbackData.create(cls, **data)).call_id
