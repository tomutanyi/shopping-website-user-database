from faker import Faker
import bcrypt
from app import app
from models import db, User, SearchHistory, Review

fake = Faker()

with app.app_context():
    # Delete existing data from the users, search histories, and reviews tables
    db.session.query(Review).delete()
    db.session.query(SearchHistory).delete()
    db.session.query(User).delete()
    
    # Reset the sequence for the id column in the users table
    db.session.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")

    db.session.commit()

    users = []
    for i in range(41):
        # Generate fake data
        username = fake.user_name()
        email = fake.email()

        # Seed only the password column
        fake_password_seeded = Faker()
        fake_password_seeded.seed_instance(i)
        plain_text_password = fake_password_seeded.password()

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
        )
        users.append(user)

        search_histories = []
        for i in range(5):
            search_history = SearchHistory(
                search_query=fake.word(),
                timestamp=fake.date_time_this_year(),
                user=user
            )
            search_histories.append(search_history)

        reviews = []
        for i in range(5):
            review = Review(
                description=fake.paragraph(),
                user=user,
                star_rating=round(fake.random.uniform(1.0, 5.0), 2)
            )
            reviews.append(review)

    db.session.add_all(users)
    db.session.add_all(search_histories)
    db.session.add_all(reviews)
    db.session.commit()
