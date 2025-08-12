from typing import Generic, TypeVar, List, Sequence

from pydantic import Field
from pydantic import BaseModel

M = TypeVar("M")


class PaginatedResponse(BaseModel, Generic[M]):
    count: int = Field(description="Number of items returned in the response")
    items: Sequence[M] = Field(
        description="List of items returned in the response following given criteria"
    )
