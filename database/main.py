import psycopg2
import json

# Establishing the connection
connection = psycopg2.connect(
    user="postgres",
    password="post",
    host="127.0.0.1",
    port="5432",
    database="limited"
)

def connect():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print(f"You are connected to - {record}\n")
        #create_tables()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def create_tables():
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            pid VARCHAR(255) PRIMARY KEY,
            sku VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            price INTEGER NOT NULL,
            image VARCHAR(255),
            quantity INTEGER NOT NULL,
            deleted BOOLEAN DEFAULT FALSE,
            updated_price BOOLEAN DEFAULT FALSE,
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sizes (
            comb_id VARCHAR(255) PRIMARY KEY,
            pid VARCHAR(255) REFERENCES products(pid) ON DELETE CASCADE,
            stock INTEGER NOT NULL,
            name VARCHAR(255),
            updated_stock BOOLEAN DEFAULT FALSE,
        );
        """)
        connection.commit()
        print("Tables created successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while creating tables", error)

def add_product(pid, sku, name, price, image, quantity, deleted=False, updated_price=False):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (pid, sku, name, price, image, quantity, deleted, updated_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (pid, sku, name, price, image, quantity, deleted, updated_price)
        )
        connection.commit()
        print(f"Product {pid} added successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while adding product to database", error)

def add_size(comb_id, pid, stock, name, updated_size=False):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO sizes (comb_id, pid, stock, name, updated_size) VALUES (%s, %s, %s, %s, %s)",
            (comb_id, pid, stock, name, updated_size)
        )
        connection.commit()
        print(f"Size {comb_id} added successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while adding size to database", error)
        if connection:
            connection.rollback()

def get_product(pid):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE pid = %s", (pid,))
        return cursor.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving product from database", error)
        return None

def get_size(comb_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sizes WHERE comb_id = %s", (comb_id,))
        return cursor.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving size from database", error)
        return None

def delete_product(pid):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE pid = %s", (pid,))
        connection.commit()
        print(f"Product {pid} deleted successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while deleting product from database", error)

def delete_size(comb_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sizes WHERE comb_id = %s", (comb_id,))
        connection.commit()
        print(f"Size {comb_id} deleted successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while deleting size from database", error)

def add_product_to_db(data):
    try:
        product_data = json.loads(data)

        # Add the product using the product data extracted from the JSON
        add_product(
            pid=product_data['pid'],
            sku=product_data['sku'],
            name=product_data['name'],
            price=product_data['price'],
            image=product_data['image'],
            quantity=product_data['quantity'],
            deleted=product_data.get('deleted'),
            updated_price=product_data.get('updated_price')
        )

        # Add each size for the product
        for size in product_data['sizes']:
            add_size(
                comb_id=size['combId'],
                pid=product_data['pid'],
                stock=size['stock'],
                name=size['name'],
                updated_size=size.get('updated_size')
            )

        print("Product and sizes added to the database successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while adding product and sizes to the database:", error)
    
def get_all_product_ids(table):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT pid FROM {table}")
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while getting all IDs from database", error)
        return []
    

def update_product_price(pid, new_price):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE products 
            SET price = %s, updated_price = TRUE 
            WHERE pid = %s
        """, (new_price, pid))
        connection.commit()
        print(f"Product {pid} price updated successfully and marked as changed.")
    except (Exception, psycopg2.Error) as error:
        print("Error while updating product price in database", error)


def update_product_quantity(pid, new_quantity):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE products SET quantity = %s WHERE pid = %s", (new_quantity, pid))
        connection.commit()
        print(f"Product {pid} quantity updated successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while updating product quantity in database", error)


def find_size_and_update_stock(pid, comb_id, new_stock):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE sizes SET stock = %s WHERE comb_id = %s AND pid = %s", (new_stock, comb_id, pid))
        connection.commit()
        print(f"Size {comb_id} stock updated successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while updating size stock in database", error)