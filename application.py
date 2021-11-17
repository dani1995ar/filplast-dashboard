from operator import length_hint
from argon2 import PasswordHasher
from flask import Flask, flash, redirect, render_template, request, jsonify
from sqlalchemy.sql.expression import false
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import cop, apology, result_to_dicts, new_order
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

@app.route("/create-order", methods=["GET", "POST"])
def create_orders():

    # Check if the name of the customer is on the database exactly as
    # it appears, AND that there is only one item that matches the search
    # if there are more, the full name is probably incomplete
    # if there are less the client is not yet in the database.
    def is_customer_on_db(customer_name):
        query = text("SELECT full_name FROM person WHERE full_name = :cn")
        if len(db.session.connection().execute(query, cn=customer_name).all()) == 1:
            return True
        return False

    if request.method == "GET":
        query = text("SELECT id, name FROM product")
        products = db.session.connection().execute(query).all()
        return render_template("create-order.html", products=products)

    elif request.method == "POST":

        # Save the form data, so we don't have to query it multiple times.
        order_data = request.form

        try:
            if (int(order_data['quantity']) > 0 
            and is_customer_on_db(order_data['full-name'])):

                # The create order form has 4 inputs by default, if there are more we know that
                # the order contains more than 1 item.
                # If there iss only 1 item in the order, then:
                dict_of_order_data = {}
                for data in order_data:
                    dict_of_order_data[data] = order_data[data]
                dict_of_order_data['total_order_item_price'] = 0
                dict_of_order_data['amount_of_items'] = 0
                print(dict_of_order_data)
                new_order(dict_of_order_data)
                return redirect("/")
            return apology("Incorrect name, product or amount")

        except ValueError:
            return apology("Not a possitive int for amount of product")


@app.route("/search", methods=["GET", "POST"])
def search():
    
    template = "search.html"
    search_type = request.args.get("type")

    def get_orders_by_customer_name(name):
        query = text(
        """SELECT o.note, o.id, p.full_name, pr.name, oi.quantity, cp.price FROM `order` AS o
        INNER JOIN person AS p ON o.person_id = p.id
        JOIN order_item AS oi ON oi.order_id = o.id
        JOIN product AS pr ON  pr.id = oi.product_id
        JOIN cost_price AS cp ON cp.product_id = pr.id
        WHERE p.full_name LIKE :pn""")
        
        # Person_name is the searched item, with SQL placeholders
        person_name = {"pn": "%" + name + "%"}
        result = db.session.connection().execute(query, person_name).all()
        print(result)
        orders = result_to_dicts(result)
        return orders

    
    def name_suggestion(partial_name):
        query = text(
        """SELECT full_name FROM person
        WHERE full_name LIKE :pn""")

        # partial_name is the data typed so far in the input field of create order
        name = {"pn": "%" + partial_name + "%"}
        suggestion = db.session.connection().execute(query, name).all()
        return suggestion

        
    # Search for name using search bar
    if request.method == "POST":
        orders = get_orders_by_customer_name(request.form.get("search"))
        if len(orders) < 1:
            return apology("No one found")
        return render_template(template, orders=orders)

    # Search for order id usgin <a> in orders number in orders template
    if search_type == "order-id":
        query = text(
        """SELECT o.note, o.id, p.full_name, pr.name, oi.quantity, cp.price FROM `order` AS o
        INNER JOIN person AS p ON o.person_id = p.id
        JOIN order_item AS oi ON oi.order_id = o.id
        JOIN product AS pr ON  pr.id = oi.product_id
        JOIN cost_price AS cp ON cp.product_id = pr.id
        WHERE o.id = :order_id;""")
        order_id = request.args.get("q")
        result = db.session.connection().execute(query, order_id=order_id).all()
        print(result)
        orders = result_to_dicts(result)
        return render_template(template, orders=orders)

    # Client/person full name search usign <a> from orders template
    elif search_type == "full-name":
        orders = get_orders_by_customer_name(request.args.get("q"))
        return render_template(template, orders=orders)

    # Name suggestion for create order input field "full-name"
    elif search_type == "suggestion":
        q = request.args.get("q")
        if q:
            name_list = name_suggestion(q)
            json = []
            for name in name_list:
                json.append(name.full_name)
            return jsonify(json)
            
        return jsonify([])
    
    return apology("There was a problem")

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

