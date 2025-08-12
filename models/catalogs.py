from datetime import datetime
from typing import Sequence

from sqlalchemy import insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlmodel import Field, SQLModel, DateTime, select

from models import Product
from schemas.catalogs import CatalogWIthProductCount


class Catalog(SQLModel, table=True):
    catalog_id: int | None = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"nullable": False},
        sa_type=DateTime
    )

    @classmethod
    async def all(cls, db: AsyncSession, limit: int = 100, offset: int = 0) -> Sequence["CatalogWIthProductCount"]:
        product_alias = aliased(Product)

        statement = (
            select(
                cls,
                func.count(product_alias.product_id).label("products_count")
            )
            .outerjoin(product_alias, product_alias.catalog_id == cls.catalog_id)
            .group_by(cls.catalog_id)
            .order_by(cls.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await db.execute(statement)
        rows = result.all()
        return [
            CatalogWIthProductCount(
                **catalog.dict(),
                products_count=products_count
            )
            for catalog, products_count in rows
        ]

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
        values = [c.model_dump(exclude_unset=True) for c in catalogs]
        stmt = (
            insert(Catalog)
            .values(values)
            .returning(Catalog)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalars().all()

    async def update(self, db, name: str):
        self.name = name
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db):
        await db.delete(self)
        await db.commit()
