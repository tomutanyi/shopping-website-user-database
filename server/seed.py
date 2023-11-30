from faker import Faker
import random
from app import app

from models import db, VendorProduct, Vendor, Product  # Add necessary imports

fake = Faker()

def generate_cost(base_cost):
    return round(base_cost * random.uniform(0.85, 1.15), 2)

def generate_rating():
    return random.uniform(1, 5)

def generate_payment_mode():
    payment_modes = ["Cash", "Paypal", "Credit Card", "M-Pesa", "PesaPal", "JamboPay"]
    return random.choice(payment_modes)

def generate_discount():
    return random.randint(0, 51)

with app.app_context():
    # Delete existing data from the vendor_products table
    db.session.query(VendorProduct).delete()

    vendor_products = []
    for vendor_id in range(1, 9):
        for product_id in range(3, 556):
            print(f"Trying to find product with ID: {product_id}")
            # Fetching product details from the product table
            product = db.session.query(Product).filter_by(id=product_id).first()

            if product is None:
                print(f"No product found with ID {product_id}")
                continue

            # Generate fake data for vendor_products
            cost = generate_cost(product.base_cost)
            rating = generate_rating()
            delivery_cost = random.uniform(5, 20)
            mode_of_payment = generate_payment_mode()
            discount = generate_discount()
            description = f"Description for Vendor {vendor_id} and Product {product_id}"

            vendor_product = VendorProduct(
                vendor_id=vendor_id,
                product_id=product_id,
                cost=cost,
                rating=rating,
                delivery_cost=delivery_cost,
                mode_of_payment=mode_of_payment,
                discount=discount,
                description=description,
            )
            vendor_products.append(vendor_product)

    db.session.add_all(vendor_products)
    db.session.commit()
