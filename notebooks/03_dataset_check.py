import pandas as pd

# SUPERMARKET SALES - BASIC DATA ANALYSIS

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
print("       SUPERMARKET SALES ANALYSIS")


# 1. Dataset Information
print("\n1. DATASET INFORMATION")
print("Number of transactions:", len(df))
print("Number of columns:", len(df.columns))

# 2. Total Sales
total_sales = df["Sales"].sum()
print("\n2. TOTAL SALES")
print("Total Sales:", round(total_sales, 2))

# 3. Average Sales
average_sales = df["Sales"].mean()
print("\n3. AVERAGE SALES PER TRANSACTION")
print("Average Sales:", round(average_sales, 2))

# 4. Total Quantity Sold
total_quantity = df["Quantity"].sum()
print("\n4. TOTAL QUANTITY SOLD")
print("Total Quantity:", total_quantity)

# 5. Average Quantity
average_quantity = df["Quantity"].mean()
print("\n5. AVERAGE QUANTITY PER TRANSACTION")
print("Average Quantity:", round(average_quantity, 2))

# 6. Total Gross Income
total_income = df["gross income"].sum()
print("\n6. TOTAL GROSS INCOME")
print("Gross Income:", round(total_income, 2))

# 7. Average Rating
average_rating = df["Rating"].mean()
print("\n7. AVERAGE CUSTOMER RATING")
print("Average Rating:", round(average_rating, 2))

# 8. Product Line Sales
product_sales = df.groupby("Product line")["Sales"].sum().sort_values(
    ascending=False
)

print("\n8. SALES BY PRODUCT LINE")
print(product_sales)

# 9. Branch Sales
branch_sales = df.groupby("Branch")["Sales"].sum().sort_values(
    ascending=False
)
print("\n9. SALES BY BRANCH")
print(branch_sales)

# 10. Payment Method Analysis
payment_count = df["Payment"].value_counts()
print("\n10. PAYMENT METHOD USAGE")
print(payment_count)

# 11. Customer Type Analysis
customer_sales = df.groupby("Customer type")["Sales"].sum().sort_values(
    ascending=False
)
print("\n11. SALES BY CUSTOMER TYPE")
print(customer_sales)

# 12. Gender Analysis
gender_sales = df.groupby("Gender")["Sales"].sum().sort_values(
    ascending=False
)

print("\n12. SALES BY GENDER")
print(gender_sales)

# 13. Monthly Sales
monthly_sales = df.groupby("Month_Name")["Sales"].sum()
print("\n13. MONTHLY SALES")
print(monthly_sales)

# 14. Hourly Sales
hourly_sales = df.groupby("Hour")["Sales"].sum().sort_values(
    ascending=False
)
print("\n14. PEAK SHOPPING HOURS")
print(hourly_sales.head(10))

# 15. Top Product Line
top_product = product_sales.idxmax()
print("\n15. TOP PRODUCT LINE")
print("Best-selling product line:", top_product)

# 16. Best Branch
best_branch = branch_sales.idxmax()
print("\n16. BEST PERFORMING BRANCH")
print("Best Branch:", best_branch)

# 17. Most Used Payment Method
most_used_payment = payment_count.idxmax()
print("\n17. MOST USED PAYMENT METHOD")
print("Payment Method:", most_used_payment)

# Final Message
print("       BASIC ANALYSIS COMPLETED!")