from datetime import datetime
from optparse import Option
from typing import Optional

from pydantic import BaseModel


class CatalogWIthProductCount(BaseModel):
    catalog_id: int
    name: str
    created_at: datetime
    products_count: Optional[int] = 0


class CatalogCreate(BaseModel):
    name: str
