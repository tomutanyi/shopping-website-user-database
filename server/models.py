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
    

class Vendor(db.Model, SerializerMixin):
    __tablename__ = "vendors"

    serialize_rules = ("-vendor_products.vendor",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float)

    vendor_products = db.relationship('VendorProduct', backref='vendor', lazy='dynamic')

    def __repr__(self):
        return f'<Vendor: {self.name}>'

class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    serialize_rules = ("-vendor_products.product",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String)


    vendor_products = db.relationship('VendorProduct', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product: {self.name}>'

class VendorProduct(db.Model, SerializerMixin):
    __tablename__ = "vendor_products"

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    cost = db.Column(db.Float)
    rating = db.Column(db.Float)
    delivery_cost = db.Column(db.Float)
    mode_of_payment = db.Column(db.String)
    discount = db.Column(db.Float)
    description = db.Column(db.String)
    

    def __repr__(self):
        return f'<VendorProduct: Vendor {self.vendor_id} - Product {self.product_id}>'





