# Book Review Site
A Flask website using [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/13/orm/) that allows users to review books. It makes use of [Goodreads API](https://www.goodreads.com/) to pull in ratings from a broader audience. It allows users to create an account, search books and submit a rating and a review for each book. Users can easily view their favorites books as well as popular books in the site.

![](https://github.com/agil98/Web-Development-Course/blob/master/Book%20Review%20Web%20Site/static/Login.PNG)
![](https://github.com/agil98/Web-Development-Course/blob/master/Book%20Review%20Web%20Site/static/Main.PNG)
![](https://github.com/agil98/Web-Development-Course/blob/master/Book%20Review%20Web%20Site/static/Search.PNG)
![](https://github.com/agil98/Web-Development-Course/blob/master/Book%20Review%20Web%20Site/static/Leave%20Review.PNG)
![](https://github.com/agil98/Web-Development-Course/blob/master/Book%20Review%20Web%20Site/static/Favorite%20book.PNG)

## Installation
> Clone the repo

``` git clone https://github.com/agil98/Web-Development-Course```
> Install all dependencies

``` pip install -r requirements.txt ```
> Set the environment variables, _FLASK_APP_, _DATABASE_URL_, _SECRET_KEY_ and _GOODREADS_KEY_, both obtained from the Goodreads site

## DB Schema
### Users
Column | Type
--- | ---
id | integer
name | character varying
username | character varying
password | character varying
### Books
Column | Type
--- | ---
isbn | character varying
title | character varying 
author | character varying
year | integer
### Reviews
Column | Type 
--- | ---
id | integer
book_id | character varying
user_id | character varying 
score | integer
review | character varying
