# seed.py

from faker import Faker
import random
from random import choice as rc
from app import app, db
from models import User, SearchHistory, Review, Vendor, Product, VendorProduct
from datetime import datetime

fake = Faker()

def seed_users(num_users=30):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

def seed_search_histories(users):
    search_histories = []
    for user in users:
        for _ in range(5):
            search_history = SearchHistory(
                search_query=fake.word(),
                timestamp=fake.date_time_this_year(),
                user=user
            )
            search_histories.append(search_history)
    db.session.add_all(search_histories)
    db.session.commit()

def seed_reviews(users):
    reviews = []
    for user in users:
        for _ in range(3):
            review = Review(
                description=fake.paragraph(),
                user=user,
                star_rating=round(random.uniform(1.0, 5.0), 2)
            )
            reviews.append(review)
    db.session.add_all(reviews)
    db.session.commit()

def seed_vendors(num_vendors=5):
    vendors = []
    for _ in range(num_vendors):
        vendor = Vendor(
            name=fake.company(),
            rating=round(random.uniform(3.0, 5.0), 2)
        )
        vendors.append(vendor)
    db.session.add_all(vendors)
    db.session.commit()

def seed_products(num_products=10):
    products = []
    for _ in range(num_products):
        product = Product(
            name=fake.word(),
            tags=' '.join(fake.words()),
            description=fake.sentence()
        )
        products.append(product)
    db.session.add_all(products)
    db.session.commit()

def seed_vendor_products(vendors, products):
    vendor_products = []
    for product in products:
        vendor_product = VendorProduct(
            vendor=rc(vendors),
            product=product,
            cost=round(random.uniform(10.0, 100.0), 2),
            rating=round(random.uniform(3.0, 5.0), 2),
            delivery_cost=round(random.uniform(2.0, 10.0), 2),
            mode_of_payment=rc(['Credit Card', 'PayPal', 'Cash']),
            discount=round(random.uniform(0.0, 20.0), 2),
            description=fake.sentence()
        )
        vendor_products.append(vendor_product)
    db.session.add_all(vendor_products)
    db.session.commit()

def seed_all():
    with app.app_context():
        db.create_all()

        # Seed Users
        users = User.query.all()
        if not users:
            seed_users()

        # Seed Search Histories
        if not SearchHistory.query.first():
            seed_search_histories(users)

        # Seed Reviews
        if not Review.query.first():
            seed_reviews(users)

        # Seed Vendors
        vendors = Vendor.query.all()
        if not vendors:
            seed_vendors()

        # Seed Products
        products = Product.query.all()
        if not products:
            seed_products()

        # Seed VendorProducts (Many-to-Many Relationship)
        if not VendorProduct.query.first():
            seed_vendor_products(vendors, products)

if __name__ == "__main__":
    seed_all()
