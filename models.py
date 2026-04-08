from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DECIMAL
from restaurant.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), unique=True)

    menu_items: Mapped[list['MenuItem']] = relationship(back_populates='category', cascade='all, delete-orphan')


class MenuItem(Base):
    __tablename__ = 'menu_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=200))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship(back_populates='menu_items')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='menu_item')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    total: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default='pending')

    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order', cascade='all, delete-orphan')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey('menu_items.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)

    menu_item: Mapped['MenuItem'] = relationship(back_populates='order_items')
    order: Mapped['Order'] = relationship(back_populates='order_items')