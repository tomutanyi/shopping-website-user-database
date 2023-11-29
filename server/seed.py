from faker import Faker
import bcrypt
from app import app

from models import db, User

fake = Faker()

with app.app_context():
    # Delete existing data from the users table
    db.session.query(User).delete()

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
            id=i+1,
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),  # Store the hashed password
        )
        users.append(user)

    db.session.add_all(users)
    
    db.session.commit()
