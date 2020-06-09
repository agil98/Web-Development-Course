import os

from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    input_username = request.form.get('username')
    input_password = request.form.get('password')
    user = db.execute("SELECT id FROM users WHERE username = :username AND password = :password", {"username": input_username, "password": input_password}).fetchone()
    if user is None:
        return render_template("error.html", message="Could not find that user.")
    else:
        return render_template("success.html")

@app.route("/success", methods=["POST"])
def success():
    return render_template("success.html")
