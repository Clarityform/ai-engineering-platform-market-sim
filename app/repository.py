from typing import Generic, TypeVar, Type, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        result = await self.session.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in_data: dict) -> ModelType:
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in_data: dict) -> Optional[ModelType]:
        db_obj = await self.get_by_id(id)
        if db_obj:
            for key, value in obj_in_data.items():
                setattr(db_obj, key, value)
            await self.session.flush()
            await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)
            await self.session.flush()
            return True
        return False
