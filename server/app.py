from flask import Flask, make_response,jsonify,request,session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime, timedelta
import redis
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from werkzeug.exceptions import NotFound
import os
# from dotenv import load_dotenv

# load_dotenv()

from models import db, User, Review, SearchHistory, VendorProduct, Product

app =   Flask(__name__)

bcrypt = Bcrypt(app=app)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default_secret_key")


app.config['SQLALCHEMY_DATABASE_URI']=os.environ["DATABASE_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url("redis://127.0.0.1:6379")
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True

CORS(app, supports_credentials=True)

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)


class CheckSession(Resource):
    def get(self):

        # user = User.query.get(session.get("user_id"))

        # if user:
        #     return (user.to_dict()), 200
        # else:
        #     return {}, 401

        user = User.query.filter(User.id == session.get('user_id')).first()

        if user:
            return (user.to_dict()), 200
        else:
            return {}, 401
    
api.add_resource(CheckSession, '/session', endpoint='check_session')
    
class SignUp(Resource):
    def post(self):
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']

        new_user = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password=password)
        )

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session.permanent=True


        response = make_response(
            jsonify(new_user.to_dict()),
            201
        )

        return response
        
api.add_resource(SignUp, '/signup', endpoint='signup')

# class Login(Resource):
#     def post(self):
#         email = request.get_json()['email']
#         password = request.get_json()['password']

#         user = User.query.filter_by(email=email).first()

#         # if user and (user.password == password):
#         #     session['user_id'] = user.id
#         #     session.permanent = True
#         #     response = make_response(jsonify(user.to_dict()), 200)
#         #     return response

#         # else:
#         #     return {'error': 'email or password is incorrect'},401

#         if not user:
#             return {"error": "user not found"}, 401
#         if not bcrypt.check_password_hash(user.password, password):
#             return {"error": "passwords do not match"}, 401
        
#         session["user_id"] = user.id
#         session.modified = True
        
#         response = make_response(jsonify(user.to_dict()), 200)

#         return response

class Login(Resource):
    def post(self):
        email = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"error": "user not found"}, 401


        hashed_password = generate_password_hash(password).decode('utf-8')
        # Check if the provided plaintext password matches the hashed password
        if check_password_hash(user.password, hashed_password):
            session["user_id"] = user.id
            session.modified = True

            response = make_response(jsonify(user.to_dict()), 200)
            return response
        else:
            return {"error": "passwords do not match"}, 401
        
api.add_resource(Login, '/login', endpoint='login')
        
class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None

            return {'message': 'user logged out successfully'}, 200
        
        else:
            return {'error': 'action not authorized'}, 401
        
api.add_resource(Logout, '/logout', endpoint='logout')


class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        response = make_response(
            jsonify(users),
            200
        )
        return response

    def post(self):
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()
        response = make_response(
            jsonify(new_user.to_dict()),
            201
        )

        return response
    
class UserById(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            response = make_response(
                jsonify(user.to_dict()),
                200
            )
            return response
    
api.add_resource(UserById, '/users/<int:user_id>', endpoint='user_by_id')


api.add_resource(Users, '/users', endpoint='users')

class AllReviews(Resource):
    def get(self):
        all_reviews = [review.to_dict() for review in Review.query.all()]

        response = make_response(
            jsonify(all_reviews),
            200
        )
        return response
    
api.add_resource(AllReviews, '/reviews', endpoint='all_reviews')

class UserReviews(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        user_reviews = [review.to_dict() for review in user.reviews]

        response = make_response(
            jsonify(user_reviews),
            200
        )
        return response
    
    def post(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        # Get review details from the request
        description = request.get_json().get('description')
        star_rating = request.get_json().get('star_rating')

        # Create a new review for the user
        new_review = Review(
            user_id=user.id,
            description=description,
            star_rating=star_rating
        )

        db.session.add(new_review)
        db.session.commit()

        response = make_response(
            jsonify(new_review.to_dict()),
            201
        )
        return response
    
    def patch(self, user_id, review_id):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        review = Review.query.filter_by(id=review_id, user_id=user_id).first()
        if review is None:
            return make_response(jsonify(message=f"Review with ID {review_id} not found for User {user_id}"), 404)

        # Get updated review details from the request
        new_description = request.get_json().get('description')

        # Update the review description
        review.description = new_description
        db.session.commit()

        response = make_response(
            jsonify(review.to_dict()),
            200
        )
        return response
    
    def delete(self, user_id, review_id):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        review = Review.query.filter_by(id=review_id, user_id=user_id).first()
        if review is None:
            return make_response(jsonify(message=f"Review with ID {review_id} not found for User {user_id}"), 404)

        # Delete the review
        db.session.delete(review)
        db.session.commit()

        return make_response(jsonify(message=f"Review with ID {review_id} for User {user_id} deleted"), 200)
    
    def get(self, user_id, review_id=None):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        if review_id is not None:
            # Retrieve a specific review by ID
            review = Review.query.filter_by(id=review_id, user_id=user_id).first()
            if review is None:
                return make_response(jsonify(message=f"Review with ID {review_id} not found for User {user_id}"), 404)

            response = make_response(
                jsonify(review.to_dict()),
                200
            )
            return response
        else:
            # Retrieve all reviews for the user
            user_reviews = [review.to_dict() for review in user.reviews]

            response = make_response(
                jsonify(user_reviews),
                200
            )
            return response

# Add a new endpoint for deleting a review
api.add_resource(UserReviews, '/users/<int:user_id>/reviews/<int:review_id>', endpoint='get_review_by_id')

# Existing code (unchanged)


api.add_resource(UserReviews, '/users/<int:user_id>/reviews/<int:review_id>', endpoint='delete_review')
    
api.add_resource(UserReviews, '/users/<int:user_id>/reviews/<int:review_id>', endpoint='update_review_description')
    


    
api.add_resource(UserReviews, '/users/<int:user_id>/reviews', endpoint='user_reviews')

class AllSearchQueries(Resource):
    def get(self):
        all_search_queries = [search.to_dict() for search in SearchHistory.query.all()]

        response = make_response(
            jsonify(all_search_queries),
            200
        )
        return response

api.add_resource(AllSearchQueries, '/search_queries', endpoint='all_search_queries')

class UserSearchQueries(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        user_search_queries = [search.to_dict() for search in user.search_history]

        response = make_response(
            jsonify(user_search_queries),
            200
        )
        return response

    def post(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify(message=f"User with ID {user_id} not found"), 404)

        data = request.get_json()
        search_query = data.get('search_query')

        if not search_query:
            return make_response(jsonify(message="Search query is required"), 400)

        new_search_query = SearchHistory(
            search_query=search_query,
            user=user  # You don't need to set the timestamp here; it will be set automatically by the database
        )

        db.session.add(new_search_query)
        db.session.commit()

        response = make_response(
            jsonify(message=f"Search query added for user {user_id}"),
            201
        )
        return response
    
api.add_resource(UserSearchQueries, '/users/<int:user_id>/search_queries', endpoint='user_search_queries')


class AllVendorProducts(Resource):
    def get(self):
        product_name = request.args.get('product_name')

        if product_name:
            filtered_vendor_products = VendorProduct.query \
                .join(Product) \
                .filter(Product.name.ilike(f"%{product_name}%")) \
                .all()

            if not filtered_vendor_products:
                return jsonify({'message': f'No Vendor products found for product name: {product_name}'}), 404

            response = make_response(jsonify([vp.to_dict() for vp in filtered_vendor_products]), 200)
        else:
            all_vendor_products = VendorProduct.query.all()

            if not all_vendor_products:
                return jsonify({'message': 'No Vendor products found'}), 404

            response = make_response(jsonify([vp.to_dict() for vp in all_vendor_products]), 200)

        return response
api.add_resource(AllVendorProducts, '/vendor_products', endpoint='all_vendor_products')



if __name__ == "__main__":
    app.run(port=5556, debug=True)


