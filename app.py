from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/bill")
def bill():
    return render_template("bill.html")


if __name__ == "__main__":
    app.run(debug=True)