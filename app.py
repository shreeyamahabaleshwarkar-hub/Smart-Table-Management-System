from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4

import json
from database import init_db, get_db_connection

app = Flask(__name__)

MENU_ITEMS = [
    {
        "id": 1,
        "name": "Veg Spring Rolls",
        "category": "Starters",
        "price": 120
    },
    {
        "id": 2,
        "name": "Paneer Tikka",
        "category": "Starters",
        "price": 180
    },
    {
        "id": 3,
        "name": "Veg Manchurian",
        "category": "Starters",
        "price": 160
    },
    {
        "id": 4,
        "name": "Paneer Butter Masala",
        "category": "Main Course",
        "price": 220
    },
    {
        "id": 5,
        "name": "Dal Tadka",
        "category": "Main Course",
        "price": 150
    },
    {
        "id": 6,
        "name": "Butter Naan",
        "category": "Breads",
        "price": 40
    },
    {
        "id": 7,
        "name": "Jeera Rice",
        "category": "Rice",
        "price": 120
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html", menu_items=MENU_ITEMS)


@app.route("/place-order", methods=["POST"])
def place_order():
    cart = []

    for item in MENU_ITEMS:
        quantity_field = f"quantity_{item['id']}"

        try:
            quantity = int(request.form.get(quantity_field, 0))
        except (TypeError, ValueError):
            quantity = 0

        if quantity < 0 or quantity > 10:
            return "Quantity must be between 0 and 10.", 400

        if quantity > 0:
            cart.append({
                "name": item["name"],
                "price": item["price"],
                "quantity": quantity,
                "subtotal": item["price"] * quantity
            })

    if not cart:
        return render_template(
            "menu.html",
            menu_items=MENU_ITEMS,
            error="Please select at least one item."
        ), 400

    total = sum(item["subtotal"] for item in cart)
    order_id = str(uuid4())[:8].upper()

    connection = get_db_connection()
    connection.execute(
        """
        INSERT INTO orders (order_reference, items, total)
        VALUES (?, ?, ?)
        """,
        (order_id, json.dumps(cart), total)
    )
    connection.commit()
    connection.close()

    return render_template(
        "confirmation.html",
        order_id=order_id,
        cart=cart,
        total=total
    )

@app.route("/help", methods=["GET", "POST"])
def help_page():
    error = None
    success = None

    if request.method == "POST":
        reason = request.form.get("reason", "").strip()
        message = request.form.get("message", "").strip()

        valid_reasons = [
            "Need assistance",
            "Question about menu",
            "Order-related issue",
            "Other"
        ]

        if reason not in valid_reasons:
            error = "Please select a valid reason."
        elif len(message) > 300:
            error = "Message must be 300 characters or less."
        else:
            connection = get_db_connection()
            connection.execute(
                """
                INSERT INTO help_requests (reason, message)
                VALUES (?, ?)
                """,
                (reason, message)
            )
            connection.commit()
            connection.close()

            success = "Your assistance request has been submitted!"

    return render_template(
        "help.html",
        success=success,
        error=error
    )

@app.route("/bill", methods=["GET", "POST"])
def bill():
    error = None
    success = None
    payment_method = None

    connection = get_db_connection()
    latest_order = connection.execute(
        """
        SELECT order_reference, items, total
        FROM orders
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()
    connection.close()

    if latest_order:
        bill_items = json.loads(latest_order["items"])
        bill_total = latest_order["total"]
        order_reference = latest_order["order_reference"]
    else:
        bill_items = []
        bill_total = 0
        order_reference = None

    if request.method == "POST":
        payment_method = request.form.get(
            "payment_method", ""
        ).strip()

        if payment_method not in ["UPI", "Cash"]:
            error = "Please select a valid payment method."

        elif payment_method == "UPI":
            if request.form.get("confirm_demo") == "yes":
                success = (
                    "Demo payment successful! "
                    "No real payment was made."
                )

        elif payment_method == "Cash":
            success = None

    return render_template(
        "bill.html",
        error=error,
        success=success,
        payment_method=payment_method,
        bill_items=bill_items,
        bill_total=bill_total,
        order_reference=order_reference
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
