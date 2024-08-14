from app import db
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(IST))
    shapes = db.relationship('Shape', backref='drawing', lazy=True, cascade='all, delete-orphan')

class Shape(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drawing_id = db.Column(db.Integer, db.ForeignKey('drawing.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    coordinates = db.Column(db.JSON, nullable=False)  
    annotations = db.relationship('Annotation', backref='shape', lazy=True, cascade='all, delete-orphan')

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shape_id = db.Column(db.Integer, db.ForeignKey('shape.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    position = db.Column(db.JSON, nullable=False) 
