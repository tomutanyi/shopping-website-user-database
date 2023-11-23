from faker import Faker
import random
from random import choice as rc
from app import app

from models import db, User, SearchHistory, Review

fake = Faker()

with app.app_context():

    users = []

    for _ in range(30):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
        )
        users.append(user)

    db.session.add_all(users)

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
