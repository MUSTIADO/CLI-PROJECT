import click
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Product, User, Order, CartItem, OrderItem
from auth import create_user, authenticate_user, get_user_role
from shopping_cart import add_to_cart, update_cart, view_cart, calculate_total
from orders import place_order, view_order_history, cancel_order
from inventory import check_stock_levels, restock_product
from utils import log_event, log_error

Session = sessionmaker(bind=engine)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('username')
@click.argument('password')
@click.argument('role')
def register(username, password, role):
    session = Session()
    create_user(session, username, password, role)
    click.echo(f"User '{username}' registered as {role}.")
    log_event(f"User '{username}' registered as {role}.")

@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    session = Session()
    user = authenticate_user(session, username, password)
    if user:
        click.echo(f"User '{username}' authenticated.")
        log_event(f"User '{username}' authenticated.")
    else:
        click.echo("Authentication failed.")
        log_error(f"Authentication failed for user '{username}'.")       
'''      
def perform_logout():
    # Your code to clear the session or token
    click.echo("Logged out successfully.")

@click.group()
def cli():
    """Your CLI tool."""
    pass

@cli.command()
def logout():
    """Logout from the CLI."""
    perform_logout()
'''

@click.group()
def product():
    pass

@product.command()
@click.argument('name')
@click.argument('price', type=float)
@click.argument('stock', type=int)
@click.option('--description', default="")
def add(name, price, stock, description):
    session = Session()
    product = Product(name=name, price=price, stock=stock, description=description)
    session.add(product)
    session.commit()
    click.echo(f"Product '{name}' added with price {price} and stock {stock}.")
    log_event(f"Product '{name}' added with price {price} and stock {stock}.")

@product.command()
@click.argument('product_id', type=int)
@click.option('--name')
@click.option('--price', type=float)
@click.option('--stock', type=int)
@click.option('--description')
def edit(product_id, name, price, stock, description):
    session = Session()
    product = session.query(Product).get(product_id)
    if product:
        if name:
            product.name = name
        if price:
            product.price = price
        if stock:
            product.stock = stock
        if description:
            product.description = description
        session.commit()
        click.echo(f"Product '{product_id}' updated.")
        log_event(f"Product '{product_id}' updated.")
    else:
        click.echo(f"Product '{product_id}' not found.")
        log_error(f"Product '{product_id}' not found.")

@product.command()
@click.argument('product_id', type=int)
def delete(product_id):
    session = Session()
    product = session.query(Product).get(product_id)
    if product:
        session.delete(product)
        session.commit()
        click.echo(f"Product '{product_id}' deleted.")
        log_event(f"Product '{product_id}' deleted.")
    else:
        click.echo(f"Product '{product_id}' not found.")
        log_error(f"Product '{product_id}' not found.")

@product.command()
def list():
    session = Session()
    products = session.query(Product).all()
    for product in products:
        click.echo(f"{product.id}: {product.name} - ${product.price} - Stock: {product.stock}")
    log_event("Listed all products.")

@click.group()
def cart():
    pass

@cart.command()
@click.argument('user_id', type=int)
@click.argument('product_id', type=int)
@click.argument('quantity', type=int)
def add(user_id, product_id, quantity):
    session = Session()
    success, message = add_to_cart(session, user_id, product_id, quantity)
    click.echo(message)
    if success:
        log_event(f"Added {quantity} of product '{product_id}' to cart for user '{user_id}'.")
    else:
        log_error(message)

@cart.command()
@click.argument('user_id', type=int)
@click.argument('product_id', type=int)
@click.argument('quantity', type=int)
def update(user_id, product_id, quantity):
    session = Session()
    success, message = update_cart(session, user_id, product_id, quantity)
    click.echo(message)
    if success:
        log_event(f"Updated cart for user '{user_id}', product '{product_id}' to quantity {quantity}.")
    else:
        log_error(message)

@cart.command()
@click.argument('user_id', type=int)
def view(user_id):
    session = Session()
    cart_items = view_cart(session, user_id)
    if not cart_items:
        click.echo("Cart is empty")
    for item in cart_items:
        click.echo(f"Product {item.product.name} - Quantity: {item.quantity}")
    log_event(f"Viewed cart for user '{user_id}'.")

@cart.command()
@click.argument('user_id', type=int)
def total(user_id):
    session = Session()
    total = calculate_total(session, user_id)
    click.echo(f"Total price: ${total}")
    log_event(f"Calculated total for cart of user '{user_id}'.")

@click.group()
def order():
    pass

@order.command()
@click.argument('user_id', type=int)
def place(user_id):
    session = Session()
    success, message = place_order(session, user_id)
    click.echo(message)
    if success:
        log_event(f"Order placed for user '{user_id}'.")
    else:
        log_error(message)

@order.command()
@click.argument('user_id', type=int)
def history(user_id):
    session = Session()
    orders = view_order_history(session, user_id)
    for order in orders:
        click.echo(f"Order {order.id} - Total: ${order.total_price} - Status: {order.status}")
    log_event(f"Viewed order history for user '{user_id}'.")

@order.command()
@click.argument('user_id', type=int)
@click.argument('order_id', type=int)
def cancel(user_id, order_id):
    session = Session()
    success, message = cancel_order(session, user_id, order_id)
    click.echo(message)
    if success:
        log_event(f"Cancelled order '{order_id}' for user '{user_id}'.")
    else:
        log_error(message)

@click.group()
def inventory():
    pass

@inventory.command()
def check():
    session = Session()
    low_stock_products = check_stock_levels(session)
    for product in low_stock_products:
        click.echo(f"Product '{product.name}' is low on stock: {product.stock} left")
    log_event("Checked stock levels.")

@inventory.command()
@click.argument('product_id', type=int)
@click.argument('quantity', type=int)
def restock(product_id, quantity):
    session = Session()
    success, message = restock_product(session, product_id, quantity)
    click.echo(message)
    if success:
        log_event(f"Restocked product '{product_id}' by {quantity}.")
    else:
        log_error(message)

# Register the command groups with the main CLI group
cli.add_command(product)
cli.add_command(cart)
cli.add_command(order)
cli.add_command(inventory)

if __name__ == '__main__':
    cli()
