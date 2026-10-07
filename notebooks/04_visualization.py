import pandas as pd
import plotly.express as px

# SUPERMARKET SALES - DATA VISUALIZATION

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
print("      SUPERMARKET SALES VISUALIZATION")

# 1. Sales by Product Line
product_sales = (
    df.groupby("Product line")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig1 = px.bar(
    product_sales,
    x="Product line",
    y="Sales",
    title="Sales by Product Line",
    labels={
        "Product line": "Product Category",
        "Sales": "Total Sales"
    }
)

fig1.update_layout(
    xaxis_tickangle=-30
)

fig1.show()

print("\n1. Product Line Chart Created")

# 2. Sales by Branch

branch_sales = (
    df.groupby("Branch")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    branch_sales,
    x="Branch",
    y="Sales",
    title="Sales by Branch",
    labels={
        "Branch": "Branch",
        "Sales": "Total Sales"
    }
)

fig2.show()

print("2. Branch Sales Chart Created")

# 3. Payment Method Usage

payment_data = (
    df["Payment"]
    .value_counts()
    .reset_index()
)

payment_data.columns = ["Payment", "Number of Transactions"]

fig3 = px.pie(
    payment_data,
    names="Payment",
    values="Number of Transactions",
    title="Payment Method Usage"
)

fig3.show()

print("3. Payment Method Chart Created")

# 4. Sales by Customer Type

customer_sales = (
    df.groupby("Customer type")["Sales"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    customer_sales,
    x="Customer type",
    y="Sales",
    title="Sales by Customer Type",
    labels={
        "Customer type": "Customer Type",
        "Sales": "Total Sales"
    }
)

fig4.show()

print("4. Customer Type Chart Created")

# 5. Sales by Gender

gender_sales = (
    df.groupby("Gender")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.pie(
    gender_sales,
    names="Gender",
    values="Sales",
    title="Sales Distribution by Gender"
)

fig5.show()

print("5. Gender Sales Chart Created")

# Completion Message
print("     ALL BASIC CHARTS CREATED!")