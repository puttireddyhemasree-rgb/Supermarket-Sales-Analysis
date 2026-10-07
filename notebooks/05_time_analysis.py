import pandas as pd
import plotly.express as px

# SUPERMARKET SALES - TIME BASED ANALYSIS

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")
print("       TIME-BASED SALES ANALYSIS")

# 1. Monthly Sales

monthly_sales = (
    df.groupby(["Month", "Month_Name"])["Sales"]
    .sum()
    .reset_index()
    .sort_values("Month")
)

print("\n1. MONTHLY SALES")
print(monthly_sales)

# Monthly sales chart
fig1 = px.bar(
    monthly_sales,
    x="Month_Name",
    y="Sales",
    title="Monthly Sales",
    labels={
        "Month_Name": "Month",
        "Sales": "Total Sales"
    }
)

fig1.show()

# 2. Daily Sales

daily_sales = (
    df.groupby(["Day", "Day_Name"])["Sales"]
    .sum()
    .reset_index()
    .sort_values("Day")
)

print("\n2. DAILY SALES")
print(daily_sales)

# Daily sales chart
fig2 = px.bar(
    daily_sales,
    x="Day",
    y="Sales",
    title="Sales by Day of Month",
    labels={
        "Day": "Day of Month",
        "Sales": "Total Sales"
    }
)

fig2.show()

# 3. Sales by Day Name

day_name_sales = (
    df.groupby("Day_Name")["Sales"]
    .sum()
    .reset_index()
)

print("\n3. SALES BY DAY NAME")
print(day_name_sales)

# Day name chart
fig3 = px.bar(
    day_name_sales,
    x="Day_Name",
    y="Sales",
    title="Sales by Day of Week",
    labels={
        "Day_Name": "Day",
        "Sales": "Total Sales"
    }
)

fig3.show()

# 4. Hourly Sales

hourly_sales = (
    df.groupby("Hour")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Hour")
)

print("\n4. HOURLY SALES")
print(hourly_sales)

# Hourly sales chart
fig4 = px.line(
    hourly_sales,
    x="Hour",
    y="Sales",
    markers=True,
    title="Sales by Shopping Hour",
    labels={
        "Hour": "Hour",
        "Sales": "Total Sales"
    }
)

fig4.show()

# 5. Peak Shopping Hour

peak_hour = (
    df.groupby("Hour")["Sales"]
    .sum()
    .idxmax()
)

peak_hour_sales = (
    df.groupby("Hour")["Sales"]
    .sum()
    .max()
)

print("\n5. PEAK SHOPPING HOUR")
print("Peak Hour:", peak_hour)
print("Sales During Peak Hour:", round(peak_hour_sales, 2))

# 6. Highest Sales Day

best_day = (
    df.groupby("Day_Name")["Sales"]
    .sum()
    .idxmax()
)

best_day_sales = (
    df.groupby("Day_Name")["Sales"]
    .sum()
    .max()
)

print("\n6. BEST SALES DAY")
print("------------------------------------------")
print("Best Day:", best_day)
print("Sales:", round(best_day_sales, 2))

# 7. Highest Sales Month

best_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax(),
    "Month_Name"
]

best_month_sales = monthly_sales["Sales"].max()

print("\n7. BEST SALES MONTH")
print("Best Month:", best_month)
print("Sales:", round(best_month_sales, 2))
print("       TIME ANALYSIS COMPLETED!")