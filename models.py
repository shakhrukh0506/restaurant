from sqlalchemy .orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Enum, DECIMAL
from database import Base

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, ForeignKey = True)
    name: Mapped[str] = mapped_column(String(length=100), unique= True)
    menu_items = Mapped[list['MenuItem']] = relationship(back_populates='category', cascade='all, delete-orphan')

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[float] = mapped_column(float)
    name: Mapped[str] = mapped_column(String(length=200))
    description: Mapped[str] = mapped_column(String(length=500))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='menu_item')
    category = Mapped(Category) = relationship(back_populates='menu_items')

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    total: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    order_items: Mapped[list['OrderItem']] = relationship(back_populates="order", cascade='all, delete-or[han]')


class OrderItem(Base):
    tablename = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    menu_item: Mapped[int] = mapped_column(Integer, ForeignKey("menu_items.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    order: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))

    menu_item: Mapped[MenuItem] =relationship(back_populates="order_items")
    order: Mapped[Order] = relationship(back_populates="order_items")