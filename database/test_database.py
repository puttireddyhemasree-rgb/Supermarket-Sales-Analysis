import sqlite3
from datetime import datetime

# SUPERMARKET SALES - DATABASE TEST
connection = sqlite3.connect("database/supermarket.db")
# Enable foreign key checking
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()
print("        TESTING DATABASE RELATIONSHIPS")

# 1. Get a customer
cursor.execute("""
    SELECT customer_id, name
    FROM customers
    LIMIT 1
""")
customer = cursor.fetchone()
if customer is None:
    print("No customer found.")
    connection.close()
    exit()
customer_id = customer[0]
customer_name = customer[1]
print("\n1. CUSTOMER")
print("Customer ID:", customer_id)
print("Customer Name:", customer_name)

# 2. Get a product
cursor.execute("""
    SELECT product_id, product_name, unit_price
    FROM products
    LIMIT 1
""")
product = cursor.fetchone()
if product is None:
    print("No product found.")
    connection.close()
    exit()
product_id = product[0]
product_name = product[1]
unit_price = product[2]
print("\n2. PRODUCT")
print("Product ID:", product_id)
print("Product Name:", product_name)
print("Unit Price:", unit_price)

# 3. Create a demo order
quantity = 2
total_amount = unit_price * quantity
order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
payment_method = "UPI"
cursor.execute("""
    INSERT INTO orders
    (customer_id, order_date, total_amount,
     payment_method, order_status)
    VALUES (?, ?, ?, ?, ?)
""", (
    customer_id,
    order_date,
    total_amount,
    payment_method,
    "Placed"
))

order_id = cursor.lastrowid
print("\n3. ORDER")
print("Order ID:", order_id)
print("Order Date:", order_date)
print("Total Amount:", round(total_amount, 2))
print("Payment Method:", payment_method)

# 4. Create order item
cursor.execute("""
    INSERT INTO order_items
    (order_id, product_id, quantity,
     unit_price, subtotal)
    VALUES (?, ?, ?, ?, ?)
""", (
    order_id,
    product_id,
    quantity,
    unit_price,
    total_amount
))
print("\n4. ORDER ITEM")
print("Product:", product_name)
print("Quantity:", quantity)
print("Subtotal:", round(total_amount, 2))

# 5. Create payment
cursor.execute("""
    INSERT INTO payments
    (order_id, payment_method,
     payment_status, payment_date)
    VALUES (?, ?, ?, ?)
""", (
    order_id,
    payment_method,
    "Completed",
    order_date
))
print("\n5. PAYMENT")
print("Payment Method:", payment_method)
print("Payment Status:", "Completed")

# 6. Save changes
connection.commit()
cursor.execute("""
    SELECT
        c.name,
        o.order_id,
        p.product_name,
        oi.quantity,
        oi.subtotal,
        pay.payment_method,
        pay.payment_status
    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN payments pay
        ON o.order_id = pay.order_id

    WHERE o.order_id = ?
""", (order_id,))

result = cursor.fetchone()
print("\n6. COMPLETE ORDER RELATIONSHIP")
if result:
    print("Customer:", result[0])
    print("Order ID:", result[1])
    print("Product:", result[2])
    print("Quantity:", result[3])
    print("Subtotal:", round(result[4], 2))
    print("Payment Method:", result[5])
    print("Payment Status:", result[6])

    print("\nDATABASE RELATIONSHIP TEST: SUCCESSFUL!")
else:
    print("Database relationship test failed.")
# 8. Close connection
connection.close()
print("       DATABASE TEST COMPLETED!")