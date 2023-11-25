from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-search_history.user.password", "-search_history.user.reviews", "-reviews.user.password",)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String, nullable=False)

    search_history = db.relationship('SearchHistory', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            # 'password': self.password,
        }

class SearchHistory(db.Model, SerializerMixin):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<SearchHistory: {self.search_query}>'

    def to_dict(self):
        return {
            'id': self.id,
            'search_query': self.search_query,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
        }

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    serialize_rules = ("-user.reviews",)

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    star_rating = db.Column(db.Float)

    def __repr__(self):
        return f'<Review: {self.description}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'user_id': self.user_id,
            'star_rating': self.star_rating,
        }

    

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
    # image url


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
    
    
    def to_dict(self):
        return {
            'vendor_id': self.vendor_id,
            'product_id': self.product_id,
            'cost': self.cost,
            'rating': self.rating,
            'delivery_cost': self.delivery_cost,
            'mode_of_payment': self.mode_of_payment,
            'discount': self.discount,
            'description': self.description,
            'vendor': self.vendor.name,
            'product': self.product.name,
            'product_tags': self.product.tags,
        }





