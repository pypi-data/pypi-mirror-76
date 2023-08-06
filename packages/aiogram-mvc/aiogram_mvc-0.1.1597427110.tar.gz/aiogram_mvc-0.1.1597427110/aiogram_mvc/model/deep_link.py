import pickle

from aiogram.utils.deep_linking import get_start_link
from mdocument import Document

from aiogram_mvc.config import DATABASE_NAME, mongo_client


class DeepLink(Document):
    database = DATABASE_NAME
    client = mongo_client
    collection = "deep_links"

    @property
    async def public_link(self):
        return await get_start_link(f"{self._id}")

    @classmethod
    async def create(cls, action, **kwargs) -> "DeepLink":
        return await super().create(**{
            "action": pickle.dumps(action),
            **kwargs,
        })

    @property
    def action(self):
        return pickle.loads(self["action"])
