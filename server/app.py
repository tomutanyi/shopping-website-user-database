from flask import Flask, make_response,jsonify,request,session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, User, Review, SearchHistory, VendorProduct, Product

app =   Flask(__name__)

app.config['SECRET_KEY'] ="msjahcufufrndf"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shopping.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

CORS(app)

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)


class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter_by(id=session['user_id']).first()
            return user.to_dict(), 200
        return {'error': 'resource not found'}
    
api.add_resource(CheckSession, '/session', endpoint='check_session')
    
class SignUp(Resource):
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

        session['user_id'] = new_user.id

        response = make_response(
            jsonify(new_user.to_dict()),
            201
        )

        return response
        
api.add_resource(SignUp, '/signup', endpoint='signup')

class Login(Resource):
    def post(self):
        email = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query.filter_by(email=email).first()

        if email and (user.password == password):
            session['user_id'] = user.id


            response = make_response(jsonify(user.to_dict()), 200)
            return response

        else:
            return {'error': 'email or password is incorrect'},401
        
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

        # Get search query details from the request
        search_query = request.get_json().get('search_query')

        # Create a new search query for the user
        new_search_query = SearchHistory(
            user_id=user.id,
            search_query=search_query
        )

        db.session.add(new_search_query)
        db.session.commit()

        response = make_response(
            jsonify(new_search_query.to_dict()),
            201
        )
        return response
    
    
    
api.add_resource(UserSearchQueries, '/users/<int:user_id>/search_queries', endpoint='user_search_queries')


class AllVendorProducts(Resource):
    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        product_name = request.args.get('product_name')

        query = VendorProduct.query.join(Product)

        if product_name:
            filtered_vendor_products = VendorProduct.query \
                .join(Product) \
                .filter(Product.name.ilike(f"%{product_name}%")) \
                .all()
            
            paginated_vendor_products = query.paginate(page=page, per_page=per_page, error_out=False)

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


