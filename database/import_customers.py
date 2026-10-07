import sqlite3
import pandas as pd

# IMPORT SAMPLE CUSTOMERS INTO DATABASE

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
# Connect to database
connection = sqlite3.connect("database/supermarket.db")
cursor = connection.cursor()
print("       IMPORTING CUSTOMER DATA")

# Create sample customers

customer_data = (
    df[["Customer type", "Gender"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Insert customers
for index, row in customer_data.iterrows():
    customer_number = index + 1
    name = f"Customer {customer_number}"
    email = f"customer{customer_number}@example.com"
    password = "password123"
    phone = f"90000000{customer_number:02d}"
    gender = row["Gender"]
    customer_type = row["Customer type"]

    cursor.execute("""
        INSERT OR IGNORE INTO customers
        (name, email, password, phone, gender, customer_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        password,
        phone,
        gender,
        customer_type
    ))

# Save changes
connection.commit()
print("\nCustomer data imported successfully!")
# Display customers

print("\nCUSTOMERS IN DATABASE")
cursor.execute("""
    SELECT
        customer_id,
        name,
        email,
        gender,
        customer_type
    FROM customers
""")

customers = cursor.fetchall()
for customer in customers:
    print(customer)
print("\nTotal customers:", len(customers))

# Close database
connection.close()
print("       CUSTOMER IMPORT COMPLETED!")