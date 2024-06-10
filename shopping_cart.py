# shopping_cart.py

from sqlalchemy.orm import Session, joinedload
from models import CartItem, Product

def add_to_cart(session: Session, user_id: int, product_id: int, quantity: int):
    product = session.query(Product).get(product_id)
    if not product or product.stock < quantity:
        return False, "Product not available or insufficient stock."
    
    cart_item = session.query(CartItem).filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(cart_item)
    session.commit()
    return True, "Product added to cart."

def update_cart(session: Session, user_id: int, product_id: int, quantity: int):
    cart_item = session.query(CartItem).filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return False, "Product not in cart."
    if quantity <= 0:
        session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    session.commit()
    return True, "Cart updated."

def view_cart(session: Session, user_id: int):
    cart_items = session.query(CartItem).options(joinedload(CartItem.product)).filter_by(user_id=user_id).all()
    return cart_items

def calculate_total(session: Session, user_id: int):
    cart_items = view_cart(session, user_id)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return total
