from cli import cli, product, cart, order, inventory
import database  # Add this line to import the database module

if __name__ == '__main__':
    cli.add_command(product)
    cli.add_command(cart)
    cli.add_command(order)
    cli.add_command(inventory)
    cli()
