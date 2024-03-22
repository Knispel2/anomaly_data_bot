from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from models.base_types import reaction, User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, BaseModel
from main import bot


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    TG_TOKEN: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[reaction, User])

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: str) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    async def delete_all_with_user(self, user: str) -> bool:
        search_result = self.model.find(self.model.user == user)
        if not (await search_result.count() > 0):
            return False
        await search_result.delete()
        return True

    async def find_with_user(self, name: str) -> List:
        search_result = self.model.find_many(self.model.user == name) if name != 'tg_data' else self.model.find_all()
        return search_result

    async def find_with_ztfid(self, ztf_id: str) -> Any:
        search_result = self.model.find_one(self.model.ztf_id == ztf_id)
        if await search_result.count():
            return search_result
        return False

    async def connect_user_to_tgid(self, message):
        user, tg_id = message.text, message.from_user.id
        search_result = self.model.find_one(self.model.user == user)
        if await search_result.count():
            await search_result.update(
                {"$set":
                     {
                         'tg_id': tg_id
                     }
                }
            )
            bot.send_message(message.from_user.id, "Успешно!")
        bot.send_message(message.from_user.id, "Что-то пошло не так. Вероятно, пользователь с таким именем не найден в базе")
