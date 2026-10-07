import sqlite3
import pandas as pd

# IMPORT PRODUCTS INTO DATABASE

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
# Connect to database
connection = sqlite3.connect("database/supermarket.db")
cursor = connection.cursor()
print("       IMPORTING PRODUCTS")
# Get unique product categories
products = (
    df.groupby("Product line")
    .agg(
        unit_price=("Unit price", "mean"),
        rating=("Rating", "mean")
    )
    .reset_index()
)

# Insert products
for _, row in products.iterrows():
    product_name = row["Product line"]
    product_line = row["Product line"]
    unit_price = round(row["unit_price"], 2)
    rating = round(row["rating"], 2)
    # Calculate stock from total quantity sold
    stock = int(
        df[df["Product line"] == product_line]["Quantity"].sum()
    )

    cursor.execute("""
        INSERT INTO products
        (product_name, product_line, unit_price, stock, description, rating)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_name,
        product_line,
        unit_price,
        stock,
        "Supermarket product category",
        rating
    ))

# Save changes
connection.commit()
print("\nProducts imported successfully!")
# Display products
print("\nPRODUCTS IN DATABASE")
cursor.execute("""
    SELECT product_id,
           product_name,
           product_line,
           unit_price,
           stock,
           rating
    FROM products
""")
products_in_db = cursor.fetchall()
for product in products_in_db:
    print(product)
print("\nTotal products imported:", len(products_in_db))

# Close connection
connection.close()
print("       PRODUCT IMPORT COMPLETED!")