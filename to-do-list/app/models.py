from app import db
from datetime import date

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(500), index=True, unique=True)
    Title = db.Column(db.String(500))
    Date = db.Column(db.DateTime)
    Description = db.Column(db.String(500))
    Complete = db.Column(db.Boolean, default=False)  