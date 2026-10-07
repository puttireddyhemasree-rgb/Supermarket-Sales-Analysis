import sqlite3

 # SUPERMARKET SALES - DATABASE VERIFICATION
connection = sqlite3.connect("database/supermarket.db")
cursor = connection.cursor()
print("       DATABASE VERIFICATION")
# 1. Check Tables
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""")
tables = cursor.fetchall()
print("\n1. DATABASE TABLES")
for table in tables:
    print("✓", table[0])
print("Total tables:", len(tables))

# 2. Check Customers
cursor.execute("SELECT COUNT(*) FROM customers")
customer_count = cursor.fetchone()[0]
print("\n2. CUSTOMERS")
print("Total customers:", customer_count)

# 3. Check Products
cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]
print("\n3. PRODUCTS")
print("Total products:", product_count)

# 4. Check Orders
cursor.execute("SELECT COUNT(*) FROM orders")
order_count = cursor.fetchone()[0]
print("\n4. ORDERS")
print("Total orders:", order_count)

# 5. Check Order Items
cursor.execute("SELECT COUNT(*) FROM order_items")
order_item_count = cursor.fetchone()[0]
print("\n5. ORDER ITEMS")
print("Total order items:", order_item_count)

# 6. Check Payments
cursor.execute("SELECT COUNT(*) FROM payments")
payment_count = cursor.fetchone()[0]
print("\n6. PAYMENTS")
print("Total payments:", payment_count)

# 7. Check Reviews
cursor.execute("SELECT COUNT(*) FROM reviews")
review_count = cursor.fetchone()[0]
print("\n7. REVIEWS")
print("Total reviews:", review_count)

# 8. Check Order Relationships
cursor.execute("""
    SELECT COUNT(*)
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    JOIN payments pay
        ON o.order_id = pay.order_id
""")
relationship_count = cursor.fetchone()[0]
print("\n8. DATABASE RELATIONSHIP")
print(
    "Complete connected orders:",
    relationship_count
)
# 9. Final Verification
print("          VERIFICATION RESULT")
if (
    len(tables) == 6
    and customer_count > 0
    and product_count > 0
    and order_count > 0
    and order_item_count > 0
    and payment_count > 0
    and relationship_count > 0
):
    print("✓ Database verification successful!")
    print("✓ All required tables are available.")
    print("✓ Customer data is available.")
    print("✓ Product data is available.")
    print("✓ Order data is available.")
    print("✓ Payment data is available.")
    print("✓ Database relationships are working.")
else:
    print("⚠ Some database components need checking.")
connection.close()
print("       PHASE 4 DATABASE CHECK DONE!")