import os
import requests
import json
from flask import Flask, render_template, jsonify, request, session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

# Create database models
db = SQLAlchemy()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(db.Integer, primary_key = True)
    name = Column(db.String, nullable = False)
    username = Column(db.String, unique = True, nullable = False)
    password = Column(db.String, nullable = False)

class Book(Base):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)

class Review(Base):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.String, db.ForeignKey("books.isbn"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    score = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable = False)

app = Flask(__name__)

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def check_login(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/main")
        return f(*args, **kwargs)
    return decorated_function

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("GOODREADS_KEY"):
    raise RuntimeError("GOODREADS_KEY is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv("SECRET_KEY")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Session()
Base.metadata.create_all(engine)

# Obtain api key
goodreads_api = os.getenv("GOODREADS_KEY")

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        if 'signup' in request.form:
            return render_template("signup.html", username_exists=False)
        else:
            input_username = request.form.get('username')
            input_password = request.form.get('password')
            user = db.query(User).filter(User.username==input_username and User.password==input_password).first()
            if user is None:
                return render_template("login.html", username_not_valid=True)
            else:
                session["user_id"] = user.id
                session["user_name"] = user.name
                return render_template("main.html", name=user.name)
    else:
        return render_template("login.html")

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
@login_required
def main():
    return render_template("main.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'update' in request.form:
        new_name = request.form.get('name')
        db.query(Users).filter(User.name == session['user_name']).update({User.name:new_name}, synchronize_session = True)
        db.commit()
        user.name = new_name
    return render_template("profile.html", current_user=session['user_name'])

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == 'POST':
        if 'search' in request.form:
            key_word = request.form.get('key_word')
            search = '%' + key_word + '%'
            books = db.execute("SELECT * FROM books WHERE LOWER(ISBN) LIKE LOWER(:search) OR LOWER(title) LIKE LOWER(:search) OR LOWER(author) LIKE LOWER(:search) ", {"search": search}).fetchall()
            ## Should add reviews to the book list
            return render_template('search.html', books=books, key_word=key_word)
        elif 'favorites' in request.form:
            books = db.query(Book).join(Review, Book.isbn == Review.book_id).filter(Review.score > 3)
            return render_template('search.html', books=books, key_word='Favorite books')
        else:
             return render_template("main.html")
    return render_template("main.html")


@app.route("/book/<string:isbn>", methods=["GET","POST"])
@login_required
def book(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key": goodreads_api, "isbns": isbn})
    data = res.json()
    book = db.query(Book).filter(Book.isbn==isbn).first()
    avg_rating = data['books'][0]['average_rating']
    reviews_count= data['books'][0]['reviews_count']

    if request.method == 'POST':
        score  = request.form('rating')
        review = request.form.get('review')
        review = Review(user = session['user_name'], book = book.isbn, score = int(score), review = review)
        db.add(review)
        db.commit()

    return render_template("book.html", book = book, avg_rating = avg_rating, reviews_count=reviews_count)

