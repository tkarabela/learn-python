"""
Simple webserver for writing articles in Markdown

Instructions:
Run "/create-db" first to create the database.

Features:
Flask
SQLAlchemy w/ SQLite
Markdown

References:
http://flask.pocoo.org/docs/0.10/quickstart/
https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
http://docs.sqlalchemy.org/en/rel_0_9/index.html
http://docs.sqlalchemy.org/en/rel_0_9/core/types.html
http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html
"""

import re
import os.path
from datetime import datetime
import http.client

from flask import Flask, render_template, redirect, url_for, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
import markdown

# -----------------------------------------------------------------------------
# Flask initialization
# -----------------------------------------------------------------------------

PATH_TO_DB = os.path.join(os.path.dirname(__file__), "database.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + PATH_TO_DB
db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.UnicodeText())
    ctime = db.Column(db.DateTime())

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.ctime = datetime.now()

    def word_count(self):
        return sum(1 for _ in re.finditer(r"\w+", self.text))

    def __repr__(self):
        return "<Article %r>" % self.title

# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)


@app.route("/article/<int:article_id>")
def show_article(article_id):
    article = Article.query.get(article_id)

    if article is None:
        abort(http.client.NOT_FOUND)

    html_text = markdown.markdown(article.text)
    return render_template("show-article.html", article=article, html_text=html_text)


@app.route("/article/<int:article_id>/edit", methods=["GET", "POST"])
def edit_article(article_id):
    article = Article.query.get(article_id)

    if article is None:
        abort(http.client.NOT_FOUND)

    if request.method == "POST":
        article.title = request.form["title"]
        article.text = request.form["text"]
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("show_article", article_id=article.id), http.client.FOUND)
    else:
        return render_template("edit-article.html", article=article)


@app.route("/article/<int:article_id>/delete")
def delete_article(article_id):
    article = Article.query.get(article_id)

    if article is None:
        abort(http.client.NOT_FOUND)

    db.session.delete(article)
    db.session.commit()
    app.logger.info("Deleted article #%d", article.id)
    return redirect(url_for("index"), http.client.FOUND)


@app.route("/article/new")
def new_article():
    article = Article("Untitled", "Article text goes here...")
    db.session.add(article)
    db.session.commit()
    app.logger.info("Created article #%d", article.id)
    return redirect(url_for("edit_article", article_id=article.id), http.client.FOUND)


@app.route("/create-db")
def create_db():
    db.create_all()
    app.logger.info("Created database file %s", PATH_TO_DB)
    return "Database file created."

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # app.debug = True
    app.run()
