from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4

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

    return render_template(
        "confirmation.html",
        order_id=order_id,
        cart=cart,
        total=total
    )


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/bill")
def bill():
    return render_template("bill.html")


if __name__ == "__main__":
    app.run(debug=True)