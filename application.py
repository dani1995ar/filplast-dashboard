from argon2 import PasswordHasher
from flask import Flask, flash, redirect, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import cop, apology, calculate_grand_total
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Configure application
app = Flask(__name__)
app.jinja_env.filters["cop"] = cop

# configure SQLAlchemy for the database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/filplast"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    return redirect("/orders")

@app.route("/create-orders")
def create_orders():
    return render_template("create-orders.html")

@app.route("/search", methods=["GET", "POST"])
def search():

    template = "search.html"

    def name_search(name):
        query = text(
        """SELECT o.id, p.full_name, pr.name, oi.quantity, cp.price FROM `order` AS o
        INNER JOIN person AS p ON o.person_id = p.id
        JOIN order_item AS oi ON oi.order_id = o.id
        JOIN product AS pr ON  pr.id = oi.product_id
        JOIN cost_price AS cp ON cp.product_id = pr.id
        WHERE p.full_name LIKE :pn""")
        
        # Person_name is the searched item, with SQL placeholders
        person_name = {"pn": "%" + name + "%"}
        orders = db.session.connection().execute(query, person_name).all()
        return orders

    # Search for name usign search bar
    if request.method == "POST":
        orders = name_search(request.form.get("search"))
        print (orders)
        return render_template(template, orders=orders, grand_total=calculate_grand_total(orders))

    # Search for order id usgin <a> in orders number in orders template
    if request.args.get("type") == "order-id":
        query = text(
        """SELECT o.id, p.full_name, pr.name, oi.quantity, cp.price FROM `order` AS o
        INNER JOIN person AS p ON o.person_id = p.id
        JOIN order_item AS oi ON oi.order_id = o.id
        JOIN product AS pr ON  pr.id = oi.product_id
        JOIN cost_price AS cp ON cp.product_id = pr.id
        WHERE o.id = :order_id;""")
        order_id = request.args.get("q")
        orders = db.session.connection().execute(query, order_id=order_id).all()
        return render_template(template, orders=orders, grand_total=calculate_grand_total(orders))

    # Client/person full name search usign <a> from orders template
    elif request.args.get("type") == "full-name":
        orders = name_search(request.args.get("q"))
        return render_template(template, orders=orders, grand_total=calculate_grand_total(orders))
    
    return apology("algosaliomal")

@app.route("/orders")
def orders():
    query = """\
    SELECT o.id, p.full_name, pr.name, oi.quantity, cp.price FROM `order` AS o
    INNER JOIN person AS p ON o.person_id = p.id
    JOIN order_item AS oi ON oi.order_id = o.id
    JOIN product AS pr ON  pr.id = oi.product_id
    JOIN cost_price AS cp ON cp.product_id = pr.id
    ORDER BY o.id DESC LIMIT 100;"""
    orders = db.session.connection().execute(query).all()
    return render_template("orders.html", orders=orders)


@app.route("/login", methods=["GET", "POST"])
def login():
    return apology("TODO")


def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
    

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
