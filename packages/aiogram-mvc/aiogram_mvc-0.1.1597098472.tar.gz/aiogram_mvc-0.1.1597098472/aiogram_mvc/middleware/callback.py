from mdocument import DocumentDoesntExist

from aiogram_mvc.middleware.exception import StopMiddleware
from aiogram_mvc.middleware.middleware import Middleware
from aiogram_mvc.model.call_data import CallbackData


class GetCallDataMiddleware(Middleware):
    @classmethod
    async def main(cls, call, *args, **kwargs):
        try:
            call_data = await CallbackData.one(call_id=call.data)
            return [call, *args], {**kwargs, "call_data": call_data}
        except DocumentDoesntExist:
            raise StopMiddleware()
