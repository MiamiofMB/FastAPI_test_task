import uvicorn as uvicorn
from fastapi import *
from pydantic import BaseModel
from db_funcs import check_product_amount, get_product_list, update_product, delete_product, create_product, \
    create_order, get_order_list, update_order_status
from logger import log_event
from typing import Optional

app = FastAPI()


class Product(BaseModel):
    name: str
    description: str
    price: int
    amount: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    amount: Optional[int] = None


class Order(BaseModel):
    date: str
    status: str
    p_id: int
    amount: int


class OrderUpdate(BaseModel):
    status: Optional[str] = None


@app.post("/products")
def crt_product(data: Product):
    log_event('Создаем продукт', 10, data=data)
    return create_product(data)


@app.get("/products")
def list_product():
    log_event('Получаем список продуктов', 10)
    return get_product_list()


@app.get("/products/{id}")
def list_product(id):
    log_event('Получаем инфу о товаре', 10)
    return get_product_list(id)


@app.put("/products/{id}")
def upd_product(id, data: ProductUpdate):
    log_event('Обновляем инфу о товаре', 10)
    return update_product(id, data)


@app.delete("/products/{id}")
def dlt_product(id):
    log_event('Удаляем инфу о товаре', 10)
    return delete_product(id)


@app.post("/orders")
def crt_order(data: Order):
    log_event('Создаем заказ', 10, data=data)
    if check_product_amount(data.p_id, data.amount):
        return create_order(data)
    return {"order_creation": "error", "desc": "закончились"}


@app.get("/orders")
def list_product():
    log_event('Получаем список заказов', 10)
    return get_order_list()


@app.get("/orders/{id}")
def list_product(id):
    log_event('Получаем заказ по айди', 10)
    return get_order_list(id)


@app.patch("/orders/{id}/status")
def list_product(id, data: OrderUpdate):
    log_event('Обновляем статус заказа', 10)
    return update_order_status(id, data.status)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
