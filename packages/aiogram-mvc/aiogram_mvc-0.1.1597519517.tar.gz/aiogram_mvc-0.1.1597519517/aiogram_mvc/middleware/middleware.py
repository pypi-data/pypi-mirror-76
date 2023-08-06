import functools
import typing

from aiogram_mvc.middleware import exception


class MiddlewareList:
    def __init__(self, *middleware: typing.Tuple["Middleware"]):
        self.middleware_list = middleware

    def __call__(self, func):
        nested_func = func
        for middleware in self.middleware_list:
            nested_func = middleware.decorator(nested_func)

        async def wrap(*args, **kwargs):
            try:
                return await nested_func(*args, **kwargs)
            except exception.StopMiddleware:
                return

        return wrap


class Middleware:

    @classmethod
    async def before(cls, *args, **kwargs):
        return (), {}

    @classmethod
    async def after(cls, result, *before_args, **before_kwargs):
        return result

    @classmethod
    def decorator(cls, func):
        @functools.wraps(func)
        async def wrap(*args, **kwargs):
            new_args, new_kwargs = await cls.before(*args, **kwargs)
            result = await func(*new_args, **new_kwargs)
            return await cls.after(result, *new_args, **new_kwargs)
        return wrap
