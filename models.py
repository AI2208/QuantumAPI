# -*- coding: utf-8 -*-

# models.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/QuantumAPIdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    circuit = db.Column(db.JSON)
    result = db.Column(db.JSON)

if __name__ == '__main__':
    db.create_all()
    print('Database schema created.')