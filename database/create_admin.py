import sqlite3

connection = sqlite3.connect("database/supermarket.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

connection.commit()

connection.close()

print("Admin table created successfully.")