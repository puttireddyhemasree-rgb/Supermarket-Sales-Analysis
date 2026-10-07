import pandas as pd
# SUPERMARKET SALES - DATA CLEANING

# 1. Load the original dataset
df = pd.read_csv("data/supermarket_sales.csv")
print("      SUPERMARKET SALES DATA CLEANING")


# 2. Display original dataset information
print("\n1. ORIGINAL DATASET")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# 3. Check missing values
print("\n2. MISSING VALUES")
print(df.isnull().sum().sum())

if df.isnull().sum().sum() == 0:
    print("No missing values found.")
else:
    print("Missing values found.")


# 4. Check duplicate rows
print("\n3. DUPLICATE ROWS")
duplicate_count = df.duplicated().sum()
print("Number of duplicate rows:", duplicate_count)


# 5. Remove duplicate rows
df = df.drop_duplicates()
print("Duplicate rows removed.")
print("Rows after removing duplicates:", df.shape[0])


# 6. Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
print("\n4. DATE COLUMN")
print("Date column converted successfully.")


# 7. Convert Time column
df["Time"] = pd.to_datetime(
    df["Time"],
    format="%H:%M",
    errors="coerce"
).dt.time

print("\n5. TIME COLUMN")
print("Time column converted successfully.")

# 8. Create Month column
df["Month"] = df["Date"].dt.month
print("\n6. MONTH COLUMN")
print("Month column created.")

# 9. Create Month Name column
df["Month_Name"] = df["Date"].dt.month_name()
print("\n7. MONTH NAME COLUMN")
print("Month_Name column created.")

# 10. Create Day column
df["Day"] = df["Date"].dt.day
print("\n8. DAY COLUMN")
print("Day column created.")

# 11. Create Day Name column
df["Day_Name"] = df["Date"].dt.day_name()
print("\n9. DAY NAME COLUMN")
print("Day_Name column created.")

# 12. Create Hour column
df["Hour"] = pd.to_datetime(
    df["Time"].astype(str),
    errors="coerce"
).dt.hour

print("\n10. HOUR COLUMN")
print("Hour column created.")

# 13. Check data types
print("\n11. DATA TYPES AFTER CLEANING")
print(df.dtypes)


# 14. Check missing values again
print("\n12. MISSING VALUES AFTER CLEANING")
print(df.isnull().sum())

# 15. Save cleaned dataset
output_file = "data/cleaned_sales.csv"
df.to_csv(output_file, index=False)
print("\n13. CLEANED DATASET")
print("Cleaned dataset saved successfully.")
print("File:", output_file)

# 16. Final dataset information
print("\n14. FINAL DATASET SIZE")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("       DATA CLEANING COMPLETED!")