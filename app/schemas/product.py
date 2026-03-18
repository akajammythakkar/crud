from datetime import datetime
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float = 0.0
    stock: int = 0
    is_active: bool = True
    category_id: int | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    is_active: bool | None = None
    category_id: int | None = None


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    is_active: bool
    category_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
