from argon2 import PasswordHasher
from flask import Flask, flash, redirect, render_template, request
from tempfile import mkdtemp
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

# define Order class
class Order :
    def __init__(self, order_id, customer_name, product_id, amount_purchased):
        order_number = order_id
        full_name = customer_name
        item = {product_id: amount_purchased}

@app.route("/")
def index():
    return render_template("/layout.html")

@app.route("/orders", methods=["GET", "POST"])
def orders():
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)
    Order = Base.classes.order
    orders = db.session.query(Order).all()
    return render_template("/orders.html", orders=order)


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
