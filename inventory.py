from sqlalchemy.orm import Session
from models import Product

def check_stock_levels(session: Session):
    products = session.query(Product).all()
    low_stock_products = [product for product in products if product.stock < 10]
    return low_stock_products

def restock_product(session: Session, product_id: int, quantity: int):
    product = session.query(Product).get(product_id)
    if not product:
        return False, "Product not found."
    
    product.stock += quantity
    session.commit()
    return True, "Product restocked."
