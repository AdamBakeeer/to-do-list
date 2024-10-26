from flask import Flask
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from app import models

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(assessment)

from app import views
