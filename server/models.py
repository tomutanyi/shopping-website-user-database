from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-search_history.user", "-reviews.user")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String, nullable=False)

    search_history = db.relationship('SearchHistory', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.username}>'

class SearchHistory(db.Model, SerializerMixin):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    serialize_rules = ("-user.search_history",)

    def __repr__(self):
        return f'<SearchHistory: {self.search_query}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    serialize_rules = ("-user.reviews",)

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    star_rating = db.Column(db.Float)

    def __repr__(self):
        return f'<Review: {self.description}>'
    

