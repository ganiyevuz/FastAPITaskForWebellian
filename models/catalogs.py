from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel, DateTime, select


class Catalog(SQLModel, table=True):
    catalog_id: int | None = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"nullable": False},
        sa_type=DateTime
    )

    @classmethod
    async def all(cls, db: AsyncSession) -> Sequence["Catalog"]:
        statement = select(cls)
        result = await db.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, catalog_id: int) -> "Catalog | None":
        return await db.get(cls, catalog_id)

    @classmethod
    async def create(cls, db, name: str):
        instance = cls(name=name)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    @classmethod
    async def bulk_create(cls, db, catalogs: Sequence["Catalog"]) -> Sequence["Catalog"]:
        db.add_all(catalogs)
        await db.commit()
        for catalog in catalogs:
            await db.refresh(catalog)
        return catalogs

    async def update(self, db, name: str):
        self.name = name
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db):
        await db.delete(self)
        await db.commit()
