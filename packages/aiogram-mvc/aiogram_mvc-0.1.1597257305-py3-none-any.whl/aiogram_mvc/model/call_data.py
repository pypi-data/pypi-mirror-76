import base64
import os

import pymongo
import pymongo.errors
from mdocument import Document

from aiogram_mvc.config import DATABASE_NAME, mongo_client


class CallbackData(Document):
    collection = "callback_data"
    database = DATABASE_NAME
    client = mongo_client

    @classmethod
    def create_indexes(cls):
        cls.sync_collection.create_index([
            ("call_id", pymongo.ASCENDING)
        ], unique=True)

    @staticmethod
    def generate_call_id():
        return base64.urlsafe_b64encode(os.urandom(35)).decode()

    @classmethod
    async def create(cls, view_cls, **kwargs) -> "CallbackData":
        retries = 3
        for retry_n in range(retries):
            try:
                return await super().create(**{
                    **kwargs,
                    "call_id": cls.generate_call_id(),
                    "view_cls_id": view_cls.id,
                })
            except pymongo.errors.DuplicateKeyError as e:
                if retry_n == retries - 1:
                    raise e
