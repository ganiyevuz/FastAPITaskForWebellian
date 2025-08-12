from pydantic import BaseModel


class CatalogCreate(BaseModel):
    name: str
