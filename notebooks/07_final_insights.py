import pandas as pd

# SUPERMARKET SALES - FINAL EDA INSIGHTS

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
print(" SUPERMARKET SALES - EDA INSIGHTS")

# 1. Overall Business Performance
total_sales = df["Sales"].sum()
total_quantity = df["Quantity"].sum()
total_transactions = df["Invoice ID"].nunique()
total_gross_income = df["gross income"].sum()
average_rating = df["Rating"].mean()
average_transaction = df["Sales"].mean()
print("\n1. OVERALL BUSINESS PERFORMANCE")
print("Total Sales:", round(total_sales, 2))
print("Total Quantity Sold:", total_quantity)
print("Total Transactions:", total_transactions)
print("Total Gross Income:", round(total_gross_income, 2))
print("Average Sales per Transaction:", round(average_transaction, 2))
print("Average Customer Rating:", round(average_rating, 2))

# 2. Product Performance
product_sales = (
    df.groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n2. PRODUCT PERFORMANCE")
if not product_sales.empty:
    best_product = product_sales.idxmax()
    least_product = product_sales.idxmin()

    print("Best Product Category:", best_product)
    print("Sales:", round(product_sales.max(), 2))

    print("Least Performing Category:", least_product)
    print("Sales:", round(product_sales.min(), 2))
else:
    print("No product sales data available.")

# 3. Branch Performance

branch_sales = (
    df.groupby("Branch")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n3. BRANCH PERFORMANCE")
if not branch_sales.empty:
    best_branch = branch_sales.idxmax()

    print("Best Branch:", best_branch)
    print("Sales:", round(branch_sales.max(), 2))
else:
    print("No branch sales data available.")

# 4. Customer Type Analysis
customer_type_count = df["Customer type"].value_counts()
print("\n4. CUSTOMER TYPE INSIGHTS")
if not customer_type_count.empty:
    most_common_customer = customer_type_count.idxmax()
    print("Most Common Customer Type:", most_common_customer)
    print("Number of Transactions:", customer_type_count.max())
    customer_type_sales = (
        df.groupby("Customer type")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    if not customer_type_sales.empty:
        print(
            "Customer Type with Highest Sales:",
            customer_type_sales.idxmax()
        )

# 5. Gender Analysis
gender_count = df["Gender"].value_counts()
print("\n5. GENDER INSIGHTS")
if not gender_count.empty:
    most_common_gender = gender_count.idxmax()
    print("Most Common Gender:", most_common_gender)
    print("Number of Transactions:", gender_count.max())
    gender_sales = (
        df.groupby("Gender")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    if not gender_sales.empty:
        print(
            "Gender with Highest Sales:",
            gender_sales.idxmax()
        )

# 6. Payment Method Analysis
payment_count = df["Payment"].value_counts()
print("\n6. PAYMENT INSIGHTS")
if not payment_count.empty:
    most_used_payment = payment_count.idxmax()

    print("Most Used Payment Method:", most_used_payment)
    print("Number of Transactions:", payment_count.max())

# 7. Monthly Sales
monthly_sales = (
    df.groupby(["Month", "Month_Name"])["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)
print("\n7. MONTHLY SALES INSIGHT")
if not monthly_sales.empty:
    best_month = monthly_sales.iloc[0]["Month_Name"]
    print("Best Sales Month:", best_month)
    print(
        "Sales:",
        round(monthly_sales.iloc[0]["Sales"], 2)
    )
else:
    print("No monthly sales data available.")

# 8. Day Analysis
day_sales = (
    df.groupby("Day_Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)
print("\n8. DAY INSIGHT")
if not day_sales.empty:
    best_day = day_sales.idxmax()

    print("Best Sales Day:", best_day)
    print("Sales:", round(day_sales.max(), 2))
else:
    print("No day sales data available.")

# 9. Peak Shopping Hour
hour_sales = (
    df.groupby("Hour")["Sales"]
    .sum()
    .sort_values(ascending=False)
)
print("\n9. PEAK SHOPPING HOUR")
if not hour_sales.empty:
    peak_hour = hour_sales.idxmax()
    print("Peak Hour:", peak_hour)
    print("Sales:", round(hour_sales.max(), 2))
else:
    print("No hourly sales data available.")

# 10. Customer Rating Analysis
product_rating = (
    df.groupby("Product line")["Rating"]
    .mean()
    .sort_values(ascending=False)
)
print("\n10. CUSTOMER RATING INSIGHT")
if not product_rating.empty:
    highest_rated_product = product_rating.idxmax()
    print(
        "Highest Rated Product Category:",
        highest_rated_product
    )
    print(
        "Average Rating:",
        round(product_rating.max(), 2)
    )
else:
    print("No rating data available.")

# 11. Branch and Product Analysis
branch_product_sales = (
    df.groupby(["Branch", "Product line"])["Sales"]
    .sum()
    .reset_index()
)
print("\n11. BEST BRANCH-PRODUCT COMBINATION")
if not branch_product_sales.empty:

    top_branch_product = branch_product_sales.loc[
        branch_product_sales["Sales"].idxmax()
    ]
    print("Branch:", top_branch_product["Branch"])
    print("Product:", top_branch_product["Product line"])
    print(
        "Sales:",
        round(top_branch_product["Sales"], 2)
    )
else:
    print("No branch-product data available.")

# 12. Final Business Insights
print("          FINAL BUSINESS INSIGHTS")
print("\nInsight 1:")
print("The supermarket generated total sales of",
      round(total_sales, 2))

if not product_sales.empty:
    print("\nInsight 2:")
    print(
        product_sales.idxmax(),
        "is the best-performing product category."
    )

    print("\nInsight 3:")
    print(
        product_sales.idxmin(),
        "has the lowest sales among the product categories."
    )

if not branch_sales.empty:
    print("\nInsight 4:")
    print(
        "Branch",
        branch_sales.idxmax(),
        "is the best-performing branch."
    )

if not customer_type_count.empty:
    print("\nInsight 5:")
    print(
        customer_type_count.idxmax(),
        "customers form the largest customer group."
    )

if not payment_count.empty:
    print("\nInsight 6:")
    print(
        payment_count.idxmax(),
        "is the most commonly used payment method."
    )

if not monthly_sales.empty:
    print("\nInsight 7:")
    print(
        "The highest sales occurred in",
        monthly_sales.iloc[0]["Month_Name"]
    )

if not day_sales.empty:
    print("\nInsight 8:")
    print(
        "The highest sales day is",
        day_sales.idxmax()
    )

if not hour_sales.empty:
    print("\nInsight 9:")
    print(
        "The peak shopping hour is",
        hour_sales.idxmax()
    )

if not product_rating.empty:
    print("\nInsight 10:")
    print(
        product_rating.idxmax(),
        "has the highest average customer rating."
    )

print("       FINAL EDA COMPLETED!")