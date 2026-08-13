import sqlite3
from pathlib import Path
from models import Product

DB_PATH = Path(__file__).with_name("Fox_Inventory.db")

def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = connect()

    sql = """

    CREATE TABLE IF NOT EXISTS FoxProducts (
    
    id_key INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    unit_price INTEGER NOT NULL

    )


    """
    connection.execute(sql)
    connection.commit()
    connection.close()

def add_item(item : Product):

    connection = connect()

    sql = """
        INSERT INTO FoxProducts(
        name,
        category,
        quantity,
        reorder_level,
        unit_price
        
        )
        VALUES(?, ?, ?, ?, ?)

    """

    connection.execute(sql, (item.name, item.category, item.quantity, item.reorder_level, item.unit_price))

    connection.commit()
    connection.close()

def update_column(product : Product, column_name : str, new_value : str | int):

    connection = connect()

    if column_name not in {
        "name",
        "category",
        "reorder_level",
        "unit_price"
    }:
        raise ValueError("Not a valid column name")

    sql = f"""
    UPDATE FoxProducts
    SET {column_name}=?
    WHERE id_key=?
    """

    connection.execute(sql, (new_value, product.id_key))
    connection.commit()
    connection.close()

def stock_movement(product : Product, quantity : int): 
    """
    Adds to or removes from stock levels.
    Negative ints supplied will remove stock.
    Stock levels cannot be below zero and will raise value error
    """
    connection = connect()

    cursor = connection.execute(
        """
        UPDATE FoxProducts
        SET quantity=quantity+?
        WHERE id_key=?
        AND quantity+? >= 0
        """,
        (quantity, product.id_key, quantity)
    )

    if cursor.rowcount == 0: 
        connection.close()
        raise ValueError("Stock movement cannot produce negative stock")

    connection.commit()
    connection.close()


def del_item(product : Product):
    connection = connect()

    sql = """
        DELETE FROM FoxProducts WHERE id_key=?

    """

    connection.execute(sql, (product.id_key,))
    connection.commit()
    connection.close()

def row_to_product(row):
    return Product(
        row["name"],
        row["category"],
        row["quantity"],
        row["reorder_level"],
        row["unit_price"],
        row["id_key"]
    )

def get_all_products() -> list[Product]:
    connection = connect()

    product_list = []

    for row in connection.execute("SELECT * FROM FoxProducts"):
        product_list.append(row_to_product(row))
    
    connection.close()

    return product_list

def get_lowstock_products() -> list[Product]:
    connection = connect()

    product_list = []

    for row in connection.execute("SELECT * FROM FoxProducts WHERE quantity <= reorder_level"):
        product_list.append(row_to_product(row))

    connection.close()

    return product_list


def get_one_product(id_key : int) -> Product | None:

    connection = connect()

    row = connection.execute("SELECT * FROM FoxProducts WHERE id_key=?", (id_key,)).fetchone()

    if row is None:
        connection.close()
        return None

    connection.close()

    return row_to_product(row)
    

