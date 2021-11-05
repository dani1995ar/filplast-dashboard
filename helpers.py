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



def result_to_dicts(result):
    orders = {}
    for item in result:
        if not orders.get(item.id):
            orders[item.id] = {}
        orders[item.id]['note'] = item.note
        orders[item.id]['customer_name'] = item.full_name
        if not orders[item.id].get('order_items'):
            orders[item.id]['order_items'] = []
        orders[item.id]['order_items'].append(
            {'item_name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'total': (item.price * item.quantity)})
        if not orders[item.id].get('total'):
            orders[item.id]['total'] = 0
        for order_item in orders[item.id]['order_items']:
            orders[item.id]['total'] +=  order_item['total']
    print(orders)
    return(orders)