from sqlalchemy.orm import Session
from models import Order, OrderItem, CartItem, Product

def place_order(session: Session, user_id: int):
    cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
    if not cart_items:
        return False, "Cart is empty."

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(user_id=user_id, total_price=total_price, status='Pending')
    session.add(order)
    session.commit()

    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
        session.add(order_item)
        product = session.query(Product).get(item.product_id)
        product.stock -= item.quantity
        session.delete(item)
    
    session.commit()
    return True, "Order placed successfully."

def view_order_history(session: Session, user_id: int):
    orders = session.query(Order).filter_by(user_id=user_id).all()
    return orders

def cancel_order(session: Session, user_id: int, order_id: int):
    order = session.query(Order).filter_by(id=order_id, user_id=user_id, status='Pending').first()
    if not order:
        return False, "Order not found or cannot be cancelled."

    for item in order.items:
        product = session.query(Product).get(item.product_id)
        product.stock += item.quantity
    
    session.delete(order)
    session.commit()
    return True, "Order cancelled."
