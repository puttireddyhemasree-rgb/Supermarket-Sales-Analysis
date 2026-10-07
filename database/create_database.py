import sqlite3

# SUPERMARKET SALES - DATABASE CREATION

# Create / connect to SQLite database
connection = sqlite3.connect("database/supermarket.db")
print("       SUPERMARKET DATABASE")
print("\nDatabase connected successfully!")

# Close connection
connection.close()
print("Database connection closed.")
print("\nDatabase creation step completed!")