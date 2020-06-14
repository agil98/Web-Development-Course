import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # Would be nice to add name and last name for the reviews
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    isbn = db.Column(db.String, nullable = False)
    review_count = db.Column(db.Integer, nullable = False)
    average_score = db.Column(db.Integer, nullable = False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    book = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    review = db.Column(db.String, nullable = False)