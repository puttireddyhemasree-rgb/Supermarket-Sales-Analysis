import pandas as pd
import plotly.express as px

# SUPERMARKET SALES
# PRODUCT & CUSTOMER BEHAVIOR ANALYSIS

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
print("   PRODUCT & CUSTOMER BEHAVIOR ANALYSIS")

# 1. Product Line - Sales

product_sales = (
    df.groupby("Product line")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

print("\n1. SALES BY PRODUCT LINE")
print(product_sales)

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

fig1.show()

# 2. Product Line - Quantity Sold

product_quantity = (
    df.groupby("Product line")["Quantity"]
    .sum()
    .reset_index()
    .sort_values("Quantity", ascending=False)
)

print("\n2. QUANTITY SOLD BY PRODUCT LINE")
print(product_quantity)

fig2 = px.bar(
    product_quantity,
    x="Product line",
    y="Quantity",
    title="Quantity Sold by Product Line",
    labels={
        "Product line": "Product Category",
        "Quantity": "Total Quantity Sold"
    }
)

fig2.show()

# 3. Top Selling Product Line

top_product = product_sales.iloc[0]["Product line"]
top_product_sales = product_sales.iloc[0]["Sales"]

print("\n3. TOP SELLING PRODUCT LINE")
print("Product:", top_product)
print("Sales:", round(top_product_sales, 2))

# 4. Least Selling Product Line

least_product = product_sales.iloc[-1]["Product line"]
least_product_sales = product_sales.iloc[-1]["Sales"]
print("\n4. LEAST SELLING PRODUCT LINE")
print("Product:", least_product)
print("Sales:", round(least_product_sales, 2))

# 5. Customer Type Analysis

customer_type = (
    df.groupby("Customer type")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Transactions=("Invoice ID", "count")
    )
    .reset_index()
)

print("\n5. CUSTOMER TYPE ANALYSIS")
print(customer_type)

fig3 = px.bar(
    customer_type,
    x="Customer type",
    y="Total_Sales",
    title="Sales by Customer Type",
    labels={
        "Customer type": "Customer Type",
        "Total_Sales": "Total Sales"
    }
)

fig3.show()

# 6. Gender Analysis

gender_analysis = (
    df.groupby("Gender")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Transactions=("Invoice ID", "count")
    )
    .reset_index()
)

print("\n6. GENDER ANALYSIS")
print(gender_analysis)

fig4 = px.bar(
    gender_analysis,
    x="Gender",
    y="Total_Sales",
    title="Sales by Gender",
    labels={
        "Gender": "Gender",
        "Total_Sales": "Total Sales"
    }
)

fig4.show()

# 7. Payment Method Analysis

payment_analysis = (
    df.groupby("Payment")
    .agg(
        Total_Sales=("Sales", "sum"),
        Transactions=("Invoice ID", "count")
    )
    .reset_index()
)

print("\n7. PAYMENT METHOD ANALYSIS")
print(payment_analysis)

fig5 = px.pie(
    payment_analysis,
    names="Payment",
    values="Transactions",
    title="Customer Payment Method Preference"
)

fig5.show()

# 8. Customer Rating Analysis

average_rating = df["Rating"].mean()

print("\n8. CUSTOMER RATING ANALYSIS")
print("Average Customer Rating:", round(average_rating, 2))

rating_data = (
    df.groupby("Rating")["Sales"]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    rating_data,
    x="Rating",
    y="Sales",
    title="Sales by Customer Rating",
    labels={
        "Rating": "Customer Rating",
        "Sales": "Total Sales"
    }
)

fig6.show()

# 9. Branch and Product Analysis

branch_product = (
    df.groupby(["Branch", "Product line"])["Sales"]
    .sum()
    .reset_index()
)

print("\n9. BRANCH AND PRODUCT SALES")
print(branch_product)

fig7 = px.bar(
    branch_product,
    x="Branch",
    y="Sales",
    color="Product line",
    barmode="group",
    title="Product Sales by Branch",
    labels={
        "Branch": "Branch",
        "Sales": "Total Sales",
        "Product line": "Product Category"
    }
)

fig7.show()

# 10. Final Customer Insights

most_common_customer = df["Customer type"].value_counts().idxmax()
most_common_gender = df["Gender"].value_counts().idxmax()
most_common_payment = df["Payment"].value_counts().idxmax()
print("\n10. CUSTOMER BEHAVIOR INSIGHTS")
print("Most common customer type:", most_common_customer)
print("Most common gender:", most_common_gender)
print("Most used payment method:", most_common_payment)
print("Top product line:", top_product)
print("Least selling product line:", least_product)
print(" PRODUCT & CUSTOMER ANALYSIS COMPLETED!")