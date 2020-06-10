import os

from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(db.Integer, primary_key = True)
    name = Column(db.String, nullable = False)
    username = Column(db.String, unique = True, nullable = False)
    password = Column(db.String, nullable = False)

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Session()
Base.metadata.create_all(engine)

@app.route("/")
def index():
    #return render_template("login.html")
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    input_username = request.form.get('username')
    input_password = request.form.get('password')
    user = db.query(User).filter(User.username==input_username and User.password==input_password).first()
    if user is None:
        return render_template("error.html", message="Could not find that user.")
    else:
        return render_template("success.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    input_name = request.form.get('name')
    input_username = request.form.get('username')
    input_password = request.form.get('password')
    user = db.query(User).filter(User.username==input_username).first()
    if user is None:
        user = User(name = input_name, username = input_username, password = input_password)
        db.add(user)
        db.commit()
        return render_template("success.html")
    else:
        return render_template("error.html", message="Select a new username")

@app.route("/success", methods=["POST"])
def success():
    return render_template("success.html")
