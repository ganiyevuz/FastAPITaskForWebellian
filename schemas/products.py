from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    catalog_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    catalog_id: int | None = None
