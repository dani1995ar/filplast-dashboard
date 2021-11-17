from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def cop(value):
    """Format value as COP."""
    return f"${value: ,}"


# Converts the results from the input into a dictionary of dicts, 
# with the following format:
# {order id:{'note': 'order notes', 'customer_name': 'John Smith', [{'product name': 
# {'quantity': amount of the product ordered, 'price': **int**, 'total': **int**}, 'total': **int**}}}
# refer to data_structure.txt for an example of this.
def result_to_dicts(result):
    orders = {}
    for item in result:
        if not orders.get(item.id):
            orders[item.id] = {}
        orders[item.id]['note'] = item.note
        orders[item.id]['customer_name'] = item.full_name
        if not orders[item.id].get('order_items'):
            orders[item.id]['order_items'] = []

       # Create a list, of  order items, to keep track of each
       # Of the items the order contains, and their properties
        orders[item.id]['order_items'].append(
            {'item_name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'total': (item.price * item.quantity)})

        # If no key exist for the total of the ORDER, create one
        if not orders[item.id].get('total'):
            orders[item.id]['total'] = 0
        
        # This keeps track of the order total, adding each order item's total
        # Works by adding the total of the last item added to "order_items"
        orders[item.id]['total'] +=  orders[item.id]['order_items'][-1]['total']
    return(orders)

def new_order(dict_of_order_details):
    additional_items = ''
    if dict_of_order_details['amount_of_items']:
        for i in range(dict_of_order_details['amount of items']):
            additional_items += (
            """INSERT INTO order_item
                SET order_id = @last_order_id,
                product_id = :product_id""" + i + """,
                total_order_item_price = :total_order_item_price""" + i + """,
                quantity = :quantity""" + i)

    data_to_insert = text(
        """INSERT INTO order
            SET person_id = (
                SELECT id FROM person
                WHERE full_name = :full-name),
                note = :note;
            SET @last_order_id = LAST_INSERT_ID();
            INSERT INTO order_item
            SET order_id = @last_order_id,
            product_id = :product-id,
            total_order_item_price = :total_order_item_price,
            quantity = :quantity""" + additional_items)
    try:
        db.session.connection().execute(data_to_insert, dict_of_order_details)
    except Exception:
        return apology("error in the data")
    return True