from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
PG_USER = 'postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:@localhost:5432/stocks' % PG_USER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    opening_price = db.Column(db.Float, nullable=False)

class StockPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    predicted_opening_price = db.Column(db.Float, nullable=False)

if __name__ == "__main__":
    # (Create tables for models)
    with app.app_context():
        db.create_all()