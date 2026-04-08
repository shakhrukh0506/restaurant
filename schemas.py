from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)


class CategoryOut(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    name: str = Field(max_length=200)
    price: float = Field(gt=0)
    description: Optional[str] = Field(default=None, max_length=500)
    category_id: int


class MenuItemOut(MenuItemCreate):
    id: int

    class Config:
        from_attributes = True


# ───── OrderItem ─────
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)
    order_id: Optional[int] = None


class OrderItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    total: float
    order_id: Optional[int]

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    address: str
    phone_number: str
    order_item_ids: list[int]


class OrderOut(BaseModel):
    id: int
    address: str
    phone_number: str
    total: float
    status: str
    order_items: list[OrderItemOut] = []

    class Config:
        from_attributes = True