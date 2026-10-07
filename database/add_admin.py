import sqlite3

connection = sqlite3.connect("database/supermarket.db")

try:

    connection.execute("""
        INSERT INTO admins
        (username, password)
        VALUES (?, ?)
    """, (
        "admin",
        "admin123"
    ))

    connection.commit()

    print("Admin account created successfully.")

except sqlite3.IntegrityError:

    print("Admin account already exists.")

connection.close()