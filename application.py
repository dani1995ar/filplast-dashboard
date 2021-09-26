import os

from argon2 import PasswordHasher
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, cop

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template("/layout.html")

@app.route("/orders")
def orders():
    return render_template("/orders.html")

@app.route("/login", methods=["GET", "POST"]
def login():
    return render_template("/login.html")