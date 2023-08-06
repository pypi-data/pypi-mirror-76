import functools
from abc import ABCMeta, abstractmethod

from aiogram_mvc.middleware.middleware import MiddlewareList
from aiogram_mvc.view import exception


class BaseMetaView(ABCMeta):
    register_func: callable
    handler_kwargs: dict
    middleware: MiddlewareList
    id: int

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if cls.__module__ != __name__:
            if getattr(cls, "handler_kwargs", None) is None:
                raise Exception(f"handler_kwargs is required in {cls}")
            cls.register_func(cls._validator(cls.main),
                              *getattr(cls, "custom_filters", []),
                              **cls.handler_kwargs)

    @abstractmethod
    def _validator(cls, *args, **kwargs):
        pass

    @abstractmethod
    def main(cls, *args, **kwargs):
        pass


class BaseView(metaclass=BaseMetaView):
    handler_kwargs: dict
    custom_filters: list
    middleware = MiddlewareList()
    __global_id_counter__ = 0

    def __init__(self):
        super().__init__()
        self.id = None

    @classmethod
    def _validator(cls, func):
        @functools.wraps(func)
        @cls.middleware
        async def wrap(update_obj, *args, **kwargs):
            try:
                validated_data = await cls.validate(update_obj, **kwargs)
            except exception.NotValidated:
                return
            kwargs["validated_data"] = validated_data if validated_data else {}
            return await func(update_obj, *args, **kwargs)

        return wrap

    @classmethod
    async def validate(cls, update_obj, call_data, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def main(cls, *args):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseView.__global_id_counter__ += 1
        cls.id = BaseView.__global_id_counter__
        return cls
