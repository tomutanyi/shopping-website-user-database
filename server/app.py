from flask import Flask, make_response,jsonify,request,session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, User, Review, SearchHistory, VendorProduct

app =   Flask(__name__)

app.config['SECRET_KEY'] ="msjahcufufrndf"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shopping.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

CORS(app)

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)


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
    
api.add_resource(UserSearchQueries, '/users/<int:user_id>/search_queries', endpoint='user_search_queries')

if __name__ == "__main__":
    app.run(port=5555, debug=True)


