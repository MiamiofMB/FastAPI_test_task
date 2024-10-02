from data_base import get_session, Order, OrderItem, Product
from logger import log_event
import json


def check_product_amount(p_id, amount) -> bool:
    session = get_session()
    item = session.query(Product).filter(Product.id == p_id).first()
    if item.amount - amount >= 0:
        item.amount -= amount
        session.close()
        return True
    session.close()
    return False


def create_product(data) -> dict:
    session = get_session()
    new_product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        amount=data.amount
    )
    session.add(new_product)
    try:
        session.commit()
        session.close()
        return {"product_creation": "success"}
    except Exception as exc:
        session.close()
        log_event("Ошибка при внесении изменений в базу данных", 40, error=str(exc))
        return {"product_creation": "error", "desc": exc}


def get_product_list(id=None) -> dict:
    session = get_session()
    if id != None:
        product = session.query(Product).filter(Product.id == id).first()
        return {'id': product.id, 'name': product.name, 'description': product.description,
                'price': str(product.price),
                'amount': product.amount
                }
    info = session.query(Product).all()
    products_list = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'amount': product.amount
    } for product in info]
    results_json = json.dumps(products_list)
    return json.loads(results_json)


def update_product(id, data) -> dict:
    session = get_session()
    item = session.query(Product).filter(Product.id == id).first()

    if data.name is not None: item.name = data.name
    if data.description is not None: item.description = data.description
    if data.amount is not None: item.amount = data.amount
    if data.price is not None: item.price = data.price

    try:
        session.commit()
        session.close()
        return {"product_update": "success"}
    except Exception as exc:
        session.close()
        log_event("Ошибка при обновлении информации о товаре", 40, error=exc)
        return {"product_update": "error"}


def delete_product(id):
    session = get_session()
    item = session.query(Product).filter(Product.id == id).first()
    session.delete(item)
    try:
        session.commit()
        session.close()
        return {"product_update": "success"}
    except Exception as exc:
        session.close()
        log_event("Ошибка при удалении информации о товаре", 40, error=exc)
        return {"product_delete": "error", "desc": exc}


def create_orderitem(item_id, order_id, amount) -> None:
    session = get_session()
    new_order_item = OrderItem(
        order_id=order_id,
        item_id=item_id,
        amount=amount
    )

    session.add(new_order_item)
    try:
        session.commit()
        session.close()
    except Exception as exc:
        session.close()
        log_event("Ошибка при создании Элемента заказа", 40, error=str(exc))


def create_order(data) -> dict:
    session = get_session()
    new_order = Order(
        date=data.date,
        status=data.status,
    )

    session.add(new_order)
    try:
        session.commit()
        order = session.query(Order).order_by(Order.id.desc()).first()
        create_orderitem(data.p_id, order.id, data.amount)
        session.close()
        return {"order_creation": "success"}
    except Exception as exc:
        session.close()
        log_event("Ошибка при создании заказа", 40, error=str(exc))
        return {"order_creation": "error", "desc": exc}



def get_order_list(id=None):
    session = get_session()
    if id is not None:
        order = session.query(Order).filter(Order.id == id).first()
        session.close()
        return {
            'date': order.date, 'status': order.status
        }
    orders = session.query(Order).all()

    orders_list = [{
        'id': order.id,
        'date': str(order.date),
        'status': order.status
    } for order in orders]

    results_json = json.dumps(orders_list)
    return json.loads(results_json)


def update_order_status(id, status):
    session = get_session()
    item = session.query(Order).filter(Order.id == id).first()

    if status is not None: item.status = status

    try:
        session.commit()
        session.close()
        return {"order_status_update": "success"}
    except Exception as exc:
        session.close()
        log_event("Ошибка при обновлении информации о статусе заказа", 40, error=exc)
        return {"order_status_update": "error", "desc": exc}
