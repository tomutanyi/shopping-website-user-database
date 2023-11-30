import json
from app import app
from models import db, User, Review, SearchHistory, VendorProduct

class TestApp:
    '''Flask application in flask_app.py'''

    def test_has_a_users_route(self):
        '''has an endpoint "/users"'''

        response = app.test_client().get('/users')
        assert(response.status_code == 200)

    def test_users_get_route_returns_a_list_of_users(self):
        '''returns JSON representing User objects at "/users"'''
        with app.app_context():
            user = User(
                username="marynjoki",
                email="test@mary.njoki",
                password='test-pass'
            )
            db.session.add(user)
            db.session.commit()

            response = app.test_client().get('/users')
            data = json.loads(response.data.decode())
            assert(isinstance(data, list))
            for existing_user in data:
                assert(isinstance(existing_user, dict))
                assert(existing_user['id'])
                assert(existing_user['username'])
                assert(existing_user['email'])

            db.session.delete(user)
            db.session.commit()

    def test_users_post_creates_a_user_record_in_db(self):
        '''allows users to create a User record through the "/users" POST route'''
        response = app.test_client().post(
            '/users',
            json = {
                "username": "joelnyongesa",
                "password": "test@1234",
                "email": "test@joel.email.com",
            }
        )

        with app.app_context():
            joel = User.query.filter_by(username="joelnyongesa").first()
            assert(joel.id)
            assert(joel.username == "joelnyongesa")
            assert(joel.email == "test@joel.email.com")
            assert(joel.password)

            db.session.delete(joel)
            db.session.commit()

    def test_has_a_users_by_id_route(self):
        '''has a resource available at "/users/<int:id>"'''

        response = app.test_client().get('/users/1')
        assert(response.status_code == 200)

    def test_users_by_id_returns_one_user(self):
        '''returns a JSON object representing one user object at "/users/<int:id>"'''

        response = app.test_client().get('/users/1')

        data = json.loads(response.data.decode())

        assert(isinstance(data, dict))
        assert(data['id'])
        assert(data['username'])
        assert(data['email'])

    def test_user_by_id_patch_route_updates_username(self):
        '''returns a JSON object representing an updated User object with username="tomutanyi" at "/students/<int:id>"'''
        with app.app_context():
            user_1 = User.query.filter_by(id=1).first()
            user_1.username = "user one"
            db.session.add(user_1)
            db.session.commit()

        response = app.test_client().patch(
            '/users/1',
            json = {
                "username": "tomutanyi",
            }
        )

        data = json.loads(response.data.decode())
        assert (isinstance(data, dict))
        assert(data['id'])
        assert(data['username'] == "tomutanyi")