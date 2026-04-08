from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from restaurant.schemas import (
    CategoryCreate, CategoryOut,
    MenuItemCreate, MenuItemOut,
    OrderItemCreate, OrderItemUpdate, OrderItemOut,
    OrderCreate, OrderOut,
)
from restaurant.database import Base, get_db, engine
from restaurant.models import Category, MenuItem, OrderItem, Order

Base.metadata.create_all(bind=engine)

api_router = APIRouter(prefix='/api')

@api_router.post('/categories', response_model=CategoryOut, tags=['Category'])
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@api_router.get('/categories', response_model=List[CategoryOut], tags=['Category'])
def list_categories(db: Session = Depends(get_db)):
    return db.scalars(select(Category)).all()

@api_router.post('/menu-items', response_model=MenuItemOut, tags=['MenuItem'])
def create_menu_item(data: MenuItemCreate, db: Session = Depends(get_db)):
    category = db.scalar(select(Category).where(Category.id == data.category_id))
    if not category:
        raise HTTPException(status_code=404, detail=f"{data.category_id} idli kategoriya topilmadi")

    item = MenuItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@api_router.get('/menu-items', response_model=List[MenuItemOut], tags=['MenuItem'])
def list_menu_items(db: Session = Depends(get_db)):
    return db.scalars(select(MenuItem)).all()


@api_router.get('/menu-items/{item_id}', response_model=MenuItemOut, tags=['MenuItem'])
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.scalar(select(MenuItem).where(MenuItem.id == item_id))
    if not item:
        raise HTTPException(status_code=404, detail=f"{item_id} idli menu item topilmadi")
    return item


@api_router.post('/order-items', response_model=OrderItemOut, tags=['OrderItem'])
def create_order_item(data: OrderItemCreate, db: Session = Depends(get_db)):
    menu_item = db.scalar(select(MenuItem).where(MenuItem.id == data.menu_item_id))
    if not menu_item:
        raise HTTPException(status_code=404, detail=f"{data.menu_item_id} idli menu item topilmadi")

    total = float(menu_item.price) * data.quantity
    order_item = OrderItem(
        menu_item_id=data.menu_item_id,
        quantity=data.quantity,
        order_id=data.order_id,
        total=total,
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item


@api_router.get('/order-items', response_model=List[OrderItemOut], tags=['OrderItem'])
def list_order_items(db: Session = Depends(get_db)):
    return db.scalars(select(OrderItem)).all()


@api_router.put('/order-items/{item_id}', response_model=OrderItemOut, tags=['OrderItem'])
def update_order_item(item_id: int, data: OrderItemUpdate, db: Session = Depends(get_db)):
    order_item = db.scalar(select(OrderItem).where(OrderItem.id == item_id))
    if not order_item:
        raise HTTPException(status_code=404, detail=f"{item_id} idli order item topilmadi")

    menu_item = db.scalar(select(MenuItem).where(MenuItem.id == order_item.menu_item_id))
    order_item.quantity = data.quantity
    order_item.total = float(menu_item.price) * data.quantity

    db.commit()
    db.refresh(order_item)
    return order_item


@api_router.delete('/order-items/{item_id}', tags=['OrderItem'])
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    order_item = db.scalar(select(OrderItem).where(OrderItem.id == item_id))
    if not order_item:
        raise HTTPException(status_code=404, detail=f"{item_id} idli order item topilmadi")

    db.delete(order_item)
    db.commit()
    return {"status": 204, "detail": "O'chirildi"}


@api_router.post('/orders', response_model=OrderOut, tags=['Order'])
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    order_items = []
    grand_total = 0.0

    for oi_id in data.order_item_ids:
        oi = db.scalar(select(OrderItem).where(OrderItem.id == oi_id))
        if not oi:
            raise HTTPException(status_code=404, detail=f"{oi_id} idli order item topilmadi")
        order_items.append(oi)
        grand_total += float(oi.total)

    order = Order(
        address=data.address,
        phone_number=data.phone_number,
        total=grand_total,
        status='pending',
    )
    db.add(order)
    db.flush()  # order.id ni olish uchun

    for oi in order_items:
        oi.order_id = order.id

    db.commit()
    db.refresh(order)
    return order


@api_router.get('/orders', response_model=List[OrderOut], tags=['Order'])
def list_orders(db: Session = Depends(get_db)):
    return db.scalars(select(Order)).all()


@api_router.get('/orders/{order_id}', response_model=OrderOut, tags=['Order'])
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail=f"{order_id} idli order topilmadi")
    return order