import sqlite3

# SUPERMARKET SALES - DATABASE TABLES

# Connect to database
connection = sqlite3.connect("database/supermarket.db")
cursor = connection.cursor()
print("       CREATING DATABASE TABLES")

# 1. Customers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    gender TEXT,
    customer_type TEXT DEFAULT 'Normal'
)
""")
print("\n1. Customers table created.")

# 2. Products Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_line TEXT NOT NULL,
    unit_price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    description TEXT,
    rating REAL DEFAULT 0
)
""")
print("2. Products table created.")

# 3. Orders Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    payment_method TEXT,
    order_status TEXT DEFAULT 'Placed',

    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
)
""")
print("3. Orders table created.")

# 4. Order Items Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,

    FOREIGN KEY (order_id)
    REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
)
""")
print("4. Order_Items table created.")

# 5. Payments Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    payment_method TEXT NOT NULL,
    payment_status TEXT DEFAULT 'Pending',
    payment_date TEXT,

    FOREIGN KEY (order_id)
    REFERENCES orders(order_id)
)
""")
print("5. Payments table created.")

# 6. Reviews Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    rating REAL,
    review_text TEXT,

    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
)
""")
print("6. Reviews table created.")
connection.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
# Save Changes
connection.commit()
print("       ALL TABLES CREATED SUCCESSFULLY!")
# Close database
connection.close()
print("\nDatabase connection closed.")