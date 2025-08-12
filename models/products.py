from datetime import datetime
from typing import Sequence

from sqlalchemy import insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel, DateTime, select


class Product(SQLModel, table=True):
    product_id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float | None = Field(default=0, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"nullable": False},
        sa_type=DateTime
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"nullable": False, "onupdate": datetime.now},
        sa_type=DateTime
    )

    catalog_id: int = Field(foreign_key="catalog.catalog_id")

    # @classmethod
    # async def save(cls, db: AsyncSession, instance: "Product") -> "Product":
    #     db.add(instance)
    #     await db.commit()
    #     await db.refresh(instance)
    #     return instance

    @classmethod
    async def all(cls, db: AsyncSession, limit: int = 100, offset: int = 0) -> Sequence["Product"]:
        statement = select(cls).limit(limit).offset(offset).order_by(cls.created_at.desc())
        result = await db.execute(statement)
        return result.scalars().all()

    @classmethod
    async def create(cls, db: AsyncSession, name: str, catalog_id: int):
        instance = cls(name=name, catalog_id=catalog_id)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    @classmethod
    async def bulk_create(cls, db, products: Sequence["Product"]) -> Sequence["Product"]:
        values = [p.model_dump(exclude_unset=True) for p in products]

        stmt = (
            insert(Product)
            .values(values)
            .returning(Product)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalars().all()

    async def update(self, db: AsyncSession, **kwargs):
        for attr, value in kwargs.items():
            # Check if the attribute exists and if its type matches the value's type
            if (attr_val := getattr(self, attr, None)) and type(attr_val) == type(value):
                setattr(self, attr, value)
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, product_id: int) -> "Product | None":
        return await db.get(cls, product_id)

    @classmethod
    async def filter_by_catalog(
            cls, db: AsyncSession, catalog_id: int
    ) -> Sequence["Product"]:
        statement = select(cls).where(cls.catalog_id == catalog_id)
        result = await db.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_top_products(
            cls, db: AsyncSession, top_n: int = 10, offset: int = 0
    ) -> Sequence["Product"]:
        statement = select(cls).order_by(cls.price.desc()).limit(top_n).offset(offset)
        result = await db.execute(statement)
        return result.scalars().all()

    # I did not use this method because I used the update method above
    # async def update_catalog(
    #         self, db: AsyncSession, catalog_id: int
    # ) -> "Product":
    #     if self.catalog_id == catalog_id:
    #         return self
    #     self.catalog_id = catalog_id
    #     await db.commit()
    #     await db.refresh(self)
    #     return self
