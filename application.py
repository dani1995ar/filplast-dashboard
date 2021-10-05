from re import A
from argon2 import PasswordHasher
from flask import Flask, flash, redirect, render_template, request
from tempfile import mkdtemp
from sqlalchemy.orm import session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import cop, apology
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# Configure application
app = Flask(__name__)

# configure SQLAlchemy for the database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/filplast"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
order_table = db.Table("order", db.metadata, autoload=True, autoload_with=db.engine)
person_table = db.Table("person", db.metadata, autoload=True, autoload_with=db.engine)
product_table = db.Table("product", db.metadata, autoload=True, autoload_with=db.engine)
order_item_table = db.Table("order_item", db.metadata, autoload=True, autoload_with=db.engine)


# define Order class
class Order:
    def __init__(self, order_id, customer_name, product_name, amount_purchased):
        self.order_number = order_id
        self.full_name = customer_name
        self.product_name = product_name
        self.amount_purchased = amount_purchased

@app.route("/")
def index():
    return render_template("/layout.html")

@app.route("/orders", methods=["GET", "POST"])
def orders():
    orders = []
    for x in range(1, 100):
        ph_order = db.session.query(order_table).filter_by(id=x).first()
        ph_customer = db.session.query(person_table).filter_by(id=ph_order.id).first()
        ph_order_item = db.session.query(order_item_table).filter_by(order_id=ph_order.id).first()
        ph_product_name = db.session.query(product_table).filter_by(id=ph_order_item.product_id).first()
        orders.append(
            Order(
                ph_order.id,
                ph_customer.full_name,
                ph_product_name.product_name,
                ph_order_item.quantity
            )
        )
    return render_template("/orders.html", orders=orders)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("/login.html")


def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
    

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
