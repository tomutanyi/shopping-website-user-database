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


if __name__ == "__main__":
    seed_all()
