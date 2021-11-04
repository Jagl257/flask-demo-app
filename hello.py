import os
import sys


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

abs_path = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{abs_path}/flask_demo.db"

db = SQLAlchemy(app) 

Migrate(app, db)

class Flashcards(db.Model):

    __tablename__ = "Flashcards"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    
    def save(self, commit=True):
        db.session.add(self)
        db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        db.session.commit()


@app.route("/")
def hello_world():
    return render_template("welcome.html", message="This is a Jinja variable")

@app.route("/cards")
def cards_view():
    cards = Flashcards.query.all()
    return render_template("cards.html", cards=cards)

@app.route("/card/<int:index>")
def card_view(index: int):
    card = Flashcards.query.get_or_404(index)
    return render_template("card.html", card=card)
