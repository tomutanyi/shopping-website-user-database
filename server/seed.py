from faker import Faker
import random
from random import choice as rc
from app import app

from models import db, User, SearchHistory, Review, Vendor, Product, VendorProduct

fake = Faker()

with app.app_context():

    User.query.delete()
    SearchHistory.query.delete()
    Review.query.delete()
    Vendor.query.delete()
    Product.query.delete()
    VendorProduct.query.delete()

    users = []
    for i in range(40):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
        )
        users.append(user)

    db.session.add_all(users)

    search_histories = []
    for user in users:
        for i in range(3):
            search_history = SearchHistory(
                search_query=fake.word(),
                timestamp=fake.date_time_this_year(),
                user=user
            )
            search_histories.append(search_history)

    db.session.add_all(search_histories)

    reviews = []
    for user in users:
        for i in range(2):
            review = Review(
                description=fake.paragraph(),
                user=user,
                star_rating=round(random.uniform(1.0, 5.0), 2)
            )
            reviews.append(review)

    db.session.add_all(reviews)

    vendors = []
    for i in range(20):
        vendor = Vendor(
            name=fake.company(),
            rating=round(random.uniform(3.0, 5.0), 2)
        )
        vendors.append(vendor)

    db.session.add_all(vendors)

    products = []
    for i in range(100):
        product = Product(
            name=fake.word(),
            tags=' '.join(fake.words())
        )
        products.append(product)

    db.session.add_all(products)

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
