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
    return render_template("login.html", username_not_valid=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'signup' in request.form:
        return render_template("signup.html", username_exists=False)
    else:
        input_username = request.form.get('username')
        input_password = request.form.get('password')
        user = db.query(User).filter(User.username==input_username and User.password==input_password).first()
        if user is None:
            return render_template("login.html", username_not_valid=True)
        else:
            current_user = user
            return render_template("main.html", name=user.name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'login' in request.form:
        return render_template("login.html")
    else:
        input_name = request.form.get('name')
        input_username = request.form.get('username')
        input_password = request.form.get('password')
        user = db.query(User).filter(User.username==input_username).first()
        if user is None:
            user = User(name = input_name, username = input_username, password = input_password)
            db.add(user)
            db.commit()
            return render_template("main.html")
        else:
            return render_template("signup.html", username_exists=True)

@app.route("/main", methods=["GET"])
def main():
    if 'search' in request.form:
        key_word = request.form.get('key_word')
        book = db.execute("SELECT * FROM books WHERE title LIKE '%:key_word%' OR author LIKE '%:key_word%' OR isbn LIKE '%:key_word%' OR year LIKE '%:key_word%'", 
        {"key_word": key_word})
        if book is not None:
            return render_template("test.html", message=book.name)
        else:
            return render_template("test.html", message="None found!")
    return render_template("main.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'update' in request.form:
        new_name = request.form.get('name')
        user.name = new_name
        db.commit()
    return render_template("profile.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    return render_template("test.html", message="not working")
