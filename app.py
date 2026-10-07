from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import pandas as pd
import json
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)
app.secret_key = "supermarket_secret_key"


def get_database_connection():
    connection = sqlite3.connect("database/supermarket.db")
    connection.row_factory = sqlite3.Row
    return connection


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- PRODUCTS ----------------

@app.route("/products")
def products():

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    connection = get_database_connection()

    categories = connection.execute("""
        SELECT DISTINCT product_line
        FROM products
        ORDER BY product_line
    """).fetchall()

    query = """
        SELECT *
        FROM products
        WHERE 1=1
    """

    parameters = []

    if search:
        query += " AND product_name LIKE ?"
        parameters.append("%" + search + "%")

    if category:
        query += " AND product_line = ?"
        parameters.append(category)

    query += " ORDER BY product_id"

    products = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "products.html",
        products=products,
        categories=categories,
        search=search,
        selected_category=category
    )


# ---------------- PRODUCT DETAILS ----------------

@app.route("/product/<int:product_id>")
def product_details(product_id):

    connection = get_database_connection()

    product = connection.execute("""
        SELECT *
        FROM products
        WHERE product_id = ?
    """, (product_id,)).fetchone()

    connection.close()

    if product is None:
        return "Product not found", 404

    return render_template(
        "product_details.html",
        product=product
    )


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        gender = request.form["gender"]

        connection = get_database_connection()

        try:

            connection.execute("""
                INSERT INTO customers
                (name, email, password, phone, gender, customer_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                email,
                password,
                phone,
                gender,
                "Normal"
            ))

            connection.commit()

            message = "Registration successful!"

        except sqlite3.IntegrityError:

            message = "Email already registered."

        connection.close()

    return render_template(
        "register.html",
        message=message
    )


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_database_connection()

        customer = connection.execute("""
            SELECT *
            FROM customers
            WHERE email = ? AND password = ?
        """, (email, password)).fetchone()

        connection.close()

        if customer:

            session["customer_id"] = customer["customer_id"]
            session["customer_name"] = customer["name"]

            return redirect(url_for("customer_dashboard"))

        else:

            message = "Invalid email or password."

    return render_template(
        "login.html",
        message=message
    )


# ---------------- CUSTOMER DASHBOARD ----------------

@app.route("/customer-dashboard")
def customer_dashboard():

    if "customer_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "customer_dashboard.html",
        customer_name=session["customer_name"]
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =====================================================
#                    SHOPPING CART
# =====================================================

# ---------------- ADD TO CART ----------------

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):

    # Customer must login before adding products
    if "customer_id" not in session:
        return redirect(url_for("login"))

    connection = get_database_connection()

    product = connection.execute("""
        SELECT *
        FROM products
        WHERE product_id = ?
    """, (product_id,)).fetchone()

    connection.close()

    if product is None:
        return "Product not found", 404

    # Create cart if it does not exist
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]

    product_id = str(product_id)

    if product_id in cart:

        # Increase quantity
        cart[product_id]["quantity"] += 1

    else:

        # Add new product
        cart[product_id] = {
            "product_name": product["product_name"],
            "unit_price": product["unit_price"],
            "quantity": 1
        }

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


# ---------------- CART PAGE ----------------

@app.route("/cart")
def cart():

    if "customer_id" not in session:
        return redirect(url_for("login"))

    cart_items = []
    total = 0

    if "cart" in session:

        for product_id, item in session["cart"].items():

            subtotal = item["unit_price"] * item["quantity"]

            cart_items.append({
                "product_id": product_id,
                "product_name": item["product_name"],
                "unit_price": item["unit_price"],
                "quantity": item["quantity"],
                "subtotal": subtotal
            })

            total += subtotal

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# ---------------- INCREASE QUANTITY ----------------

@app.route("/increase-cart/<int:product_id>")
def increase_cart(product_id):

    if "customer_id" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id]["quantity"] += 1

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


# ---------------- DECREASE QUANTITY ----------------

@app.route("/decrease-cart/<int:product_id>")
def decrease_cart(product_id):

    if "customer_id" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id]["quantity"] -= 1

        if cart[product_id]["quantity"] <= 0:
            del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


# ---------------- REMOVE FROM CART ----------------

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):

    if "customer_id" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


    # ---------------- CHECKOUT ----------------

@app.route("/checkout")
def checkout():

    if "customer_id" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("cart"))

    cart_items = []
    total = 0

    for product_id, item in cart.items():

        subtotal = item["unit_price"] * item["quantity"]

        cart_items.append({
            "product_id": product_id,
            "product_name": item["product_name"],
            "unit_price": item["unit_price"],
            "quantity": item["quantity"],
            "subtotal": subtotal
        })

        total += subtotal

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )
# ---------------- PLACE ORDER ----------------

@app.route("/place-order", methods=["POST"])
def place_order():

    if "customer_id" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("cart"))

    payment_method = request.form["payment_method"]

    connection = get_database_connection()

    try:

        # Calculate total amount
        total_amount = 0

        for product_id, item in cart.items():

            subtotal = item["unit_price"] * item["quantity"]

            total_amount += subtotal


        # Create order
        cursor = connection.execute("""
            INSERT INTO orders
            (
                customer_id,
                order_date,
                total_amount,
                payment_method,
                order_status
            )
            VALUES (?, datetime('now'), ?, ?, ?)
        """, (
            session["customer_id"],
            total_amount,
            payment_method,
            "Placed"
        ))

        order_id = cursor.lastrowid


        # Add products to order_items
        for product_id, item in cart.items():

            subtotal = (
                item["unit_price"] *
                item["quantity"]
            )

            connection.execute("""
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                order_id,
                product_id,
                item["quantity"],
                item["unit_price"],
                subtotal
            ))


        # Add payment information
        connection.execute("""
            INSERT INTO payments
            (
                order_id,
                payment_method,
                payment_status,
                payment_date
            )
            VALUES (?, ?, ?, datetime('now'))
        """, (
            order_id,
            payment_method,
            "Pending"
        ))


        connection.commit()

        # Clear cart after successful order
        session.pop("cart", None)

        return render_template(
            "order_confirmation.html",
            order_id=order_id,
            total_amount=total_amount,
            payment_method=payment_method
        )


    except Exception as error:

        connection.rollback()

        return f"Order could not be placed: {error}"


    finally:

        connection.close()
        # ---------------- ORDER HISTORY ----------------

@app.route("/orders")
def orders():

    if "customer_id" not in session:
        return redirect(url_for("login"))

    connection = get_database_connection()

    orders = connection.execute("""
        SELECT
            order_id,
            order_date,
            total_amount,
            payment_method,
            order_status
        FROM orders
        WHERE customer_id = ?
        ORDER BY order_id DESC
    """, (session["customer_id"],)).fetchall()

    connection.close()

    return render_template(
        "orders.html",
        orders=orders
    )
# ---------------- ADMIN LOGIN ----------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_database_connection()

        admin = connection.execute("""
            SELECT *
            FROM admins
            WHERE username = ? AND password = ?
        """, (username, password)).fetchone()

        connection.close()

        if admin:

            session["admin_id"] = admin["admin_id"]
            session["admin_username"] = admin["username"]

            return redirect(url_for("admin_dashboard"))

        else:

            message = "Invalid admin username or password."

    return render_template(
        "admin_login.html",
        message=message
    )
# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    return render_template(
        "admin_dashboard.html",
        admin_username=session["admin_username"]
    )
@app.route("/admin/products")
def admin_products():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    products = connection.execute("""
        SELECT *
        FROM products
        ORDER BY product_id
    """).fetchall()

    connection.close()

    return render_template(
        "admin_products.html",
        products=products
    )
@app.route("/admin/products/add", methods=["GET", "POST"])
def admin_add_product():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    message = ""

    if request.method == "POST":

        product_name = request.form["product_name"]
        product_line = request.form["product_line"]
        unit_price = float(request.form["unit_price"])
        stock = int(request.form["stock"])
        description = request.form["description"]
        rating = float(request.form["rating"])

        connection = get_database_connection()

        connection.execute("""
            INSERT INTO products
            (product_name, product_line, unit_price, stock, description, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product_name,
            product_line,
            unit_price,
            stock,
            description,
            rating
        ))

        connection.commit()
        connection.close()

        message = "Product added successfully!"

    return render_template(
        "admin_add_product.html",
        message=message
    )
@app.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
def admin_edit_product(product_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    product = connection.execute("""
        SELECT *
        FROM products
        WHERE product_id = ?
    """, (product_id,)).fetchone()

    if product is None:
        connection.close()
        return "Product not found", 404

    if request.method == "POST":

        product_name = request.form["product_name"]
        product_line = request.form["product_line"]
        unit_price = float(request.form["unit_price"])
        stock = int(request.form["stock"])
        description = request.form["description"]
        rating = float(request.form["rating"])

        connection.execute("""
            UPDATE products
            SET product_name = ?,
                product_line = ?,
                unit_price = ?,
                stock = ?,
                description = ?,
                rating = ?
            WHERE product_id = ?
        """, (
            product_name,
            product_line,
            unit_price,
            stock,
            description,
            rating,
            product_id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("admin_products"))

    connection.close()

    return render_template(
        "admin_edit_product.html",
        product=product
    )
@app.route("/admin/products/delete/<int:product_id>")
def admin_delete_product(product_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    connection.execute("""
        DELETE FROM products
        WHERE product_id = ?
    """, (product_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("admin_products"))
@app.route("/admin/products/stock/<int:product_id>", methods=["GET", "POST"])
def admin_update_stock(product_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    product = connection.execute("""
        SELECT *
        FROM products
        WHERE product_id = ?
    """, (product_id,)).fetchone()

    if product is None:
        connection.close()
        return "Product not found", 404

    if request.method == "POST":

        stock = int(request.form["stock"])

        connection.execute("""
            UPDATE products
            SET stock = ?
            WHERE product_id = ?
        """, (stock, product_id))

        connection.commit()
        connection.close()

        return redirect(url_for("admin_products"))

    connection.close()

    return render_template(
        "admin_update_stock.html",
        product=product
    )
@app.route("/admin/customers")
def admin_customers():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "")

    connection = get_database_connection()

    if search:

        customers = connection.execute("""
            SELECT *
            FROM customers
            WHERE name LIKE ?
               OR email LIKE ?
            ORDER BY customer_id
        """, (
            "%" + search + "%",
            "%" + search + "%"
        )).fetchall()

    else:

        customers = connection.execute("""
            SELECT *
            FROM customers
            ORDER BY customer_id
        """).fetchall()

    connection.close()

    return render_template(
        "admin_customers.html",
        customers=customers,
        search=search
    )
@app.route("/admin/customers/delete/<int:customer_id>")
def admin_delete_customer(customer_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    connection.execute("""
        DELETE FROM customers
        WHERE customer_id = ?
    """, (customer_id,))

    connection.commit()

    connection.close()

    return redirect(url_for("admin_customers"))
@app.route("/admin/orders")
def admin_orders():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    orders = connection.execute("""
        SELECT
            orders.order_id,
            customers.name AS customer_name,
            orders.order_date,
            orders.total_amount,
            orders.payment_method,
            orders.order_status
        FROM orders
        LEFT JOIN customers
        ON orders.customer_id = customers.customer_id
        ORDER BY orders.order_id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "admin_orders.html",
        orders=orders
    )
@app.route("/admin/orders/update/<int:order_id>", methods=["POST"])
def admin_update_order(order_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    order_status = request.form["order_status"]

    connection = get_database_connection()

    connection.execute("""
        UPDATE orders
        SET order_status = ?
        WHERE order_id = ?
    """, (order_status, order_id))

    connection.commit()
    connection.close()

    return redirect(url_for("admin_orders"))

@app.route("/admin/orders/<int:order_id>")
def admin_order_details(order_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    order = connection.execute("""
        SELECT
            orders.*,
            customers.name AS customer_name
        FROM orders
        LEFT JOIN customers
        ON orders.customer_id = customers.customer_id
        WHERE orders.order_id = ?
    """, (order_id,)).fetchone()

    if order is None:
        connection.close()
        return "Order not found", 404

    items = connection.execute("""
        SELECT
            order_items.*,
            products.product_name
        FROM order_items
        LEFT JOIN products
        ON order_items.product_id = products.product_id
        WHERE order_items.order_id = ?
    """, (order_id,)).fetchall()

    connection.close()

    return render_template(
        "admin_order_details.html",
        order=order,
        items=items
    )
@app.route("/admin/analytics")
def admin_analytics():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_database_connection()

    orders = connection.execute("""
        SELECT *
        FROM orders
    """).fetchall()

    connection.close()

    total_orders = len(orders)

    total_revenue = 0

    for order in orders:
        total_revenue += order["total_amount"]

    if total_orders > 0:
        average_order_value = total_revenue / total_orders
    else:
        average_order_value = 0

    return render_template(
        "admin_analytics.html",
        total_revenue=total_revenue,
        total_orders=total_orders,
        average_order_value=average_order_value
    )

if __name__ == "__main__":
    app.run(debug=True)