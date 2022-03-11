"""
config for flask app
app.config variables go here
secrets go here, but they should be secret instead****
db is assigned to a SQLAlchemy object
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{os.getcwd()}/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "this should be secret"
db = SQLAlchemy(app)
