import os
import collections
import json

from flask import Flask, request, abort, jsonify, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

from models import setup_db,Actor, Movie
from auth.auth import AuthError, requires_auth
from configs.config import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, APP_SECRET_KEY, API_AUDIENCE
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    app.config["SWAGGER"] = {
        "uiversion": 3,
    }
    SWAGGER_TEMPLATE = {
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "in": "header",
                "name": 'Authorization'
            }
        },
        "security": [
            {
                "BearerAuth": ['Authorization']
            }
        ]
    }

    Swagger(app, template=SWAGGER_TEMPLATE)
    CORS(app)
    app.secret_key = APP_SECRET_KEY
    oauth = OAuth(app)
    oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=f'https://{AUTH0_DOMAIN}',
        access_token_url=f'https://{AUTH0_DOMAIN}' + '/oauth/token',
        authorize_url=f'https://{AUTH0_DOMAIN}' + '/authorize',
        client_kwargs={
            "response_mode" : "query"
        },
        server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
    )

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    

    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        try:
            token = oauth.auth0.authorize_access_token()
            session["user"] = token
            return redirect("/home")
            
        except Exception as ex:
            print(ex)
            print('An exception occurred')
       

    @app.route("/home")
    def home():
        return render_template("home.html", pretty=json.dumps(session.get('user'), indent=4))
    
    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True),
            audience=API_AUDIENCE
        )
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/home")
    

    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def fetch_actors(payload):
        """
        get all actors
        ---
        tags:
          - actors
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        actors:
                            type: array
                            description: The awesomeness list
                            items:
                                type: object
                                properties:
                                    id:
                                        type: number
                                        description: The id of the actor
                                        default: 1
                                    name:
                                        type: string
                                        description: The name of the actor
                                        default: Steven Wilson
                                    age:
                                        type: string
                                        description: The age of the actor
                                        default: 30
                                    gender:
                                        type: string
                                        description: The gender of the actor
                                        default: Male 
              
        """
        all_actors = Actor.query.all()
        if len(all_actors) == 0:
            print('No records')
        actors = []
        for actor in all_actors:
            actors.append({
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            })
        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):
        """
        create actor
        ---
        tags:
          - actors
        parameters:
          - in: body
            name: body
            description: JSON parameters.
            schema:
              id: Actors
              required:
                - age
                - name
                - gender
              properties:
                name:
                  type: string
                  description: The name of the actor
                  default: Steven Wilson
                age:
                  type: string
                  description: The age of the actor
                  default: 30
                gender:
                  type: string
                  description: The gender of the actor
                  default: Male
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        actor:
                            type: object
                            properties:
                                name:
                                    type: string
                                    description: The name of the actor
                                    default: Steven Wilson
                                age:
                                    type: string
                                    description: The age of the actor
                                    default: 30
                                gender:
                                    type: string
                                    description: The gender of the actor
                                    default: Male
        """
        data = request.get_json()
        if data.get('name') is None or data.get('age') is None or data.get('gender') is None:
            abort(400)
        actor = Actor(name=data.get('name') , age=data.get('age'), gender=data.get('gender'))
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(payload, id):
        """
        update actor
        ---
        tags:
          - actors
        parameters:
            - in: path
              name: id
              type: string
              required: True  
            - in: body
              name: body
              description: JSON parameters.
              schema:
                id: Actors
                required:
                  - age
                  - name
                  - gender
                properties:
                  name:
                    type: string
                    description: The name of the actor
                    default: Steven Wilson
                  age:
                    type: string
                    description: The age of the actor
                    default: 30
                  gender:
                    type: string
                    description: The gender of the actor
                    default: Male
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        actor:
                            type: object
                            properties:
                                name:
                                    type: string
                                    description: The name of the actor
                                    default: Steven Wilson
                                age:
                                    type: string
                                    description: The age of the actor
                                    default: 30
                                gender:
                                    type: string
                                    description: The gender of the actor
                                    default: Male
        """
        data = request.get_json()
        if data.get('name') is None or data.get('age') is None or data.get('gender') is None:
            abort(400)
        actor = Actor.query.get(id)
        if actor == None:
            abort(404)
        actor.name = data.get('name')
        actor.age = data.get('age')
        actor.gender = data.get('gender') 
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        """
        delete actor
        ---
        tags:
          - actors
        parameters:
            - in: path
              name: id
              type: string
              required: True  
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        id:
                            type: string
                            description: The language name
                            default: 1
                             
        """
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'id': id
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def fetch_movies(payload):
        """
        get all movies
        ---
        tags:
          - movies
        responses:
          200:
            description: OK
            schema:
                properties:
                        success:
                            type: boolean
                            default: True
                        movies:
                            type: object
                            properties:
                                id:
                                    type: number
                                    description: The id of the movie
                                    default: 1
                                title:
                                    type: string
                                    description: The name of the movie
                                    default: Steven Wilson
                                release:
                                    type: string
                                    description: The release of the movie
                                    default: 30
        """
        all_movies = Movie.query.all()
        if len(all_movies) == 0:
            abort(404)
        movies = []
        for movie in all_movies:
            movies.append({
                'id': movie.id,
                'title': movie.title,
                'release': movie.release,
            })
        return jsonify({
            'success': True,
            'movies': movies
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        """
        delete movie
        ---
        tags:
          - movies
        parameters:
            - in: path
              name: id
              type: string
              required: True  
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        id:
                            type: string
                            description: The language name
                            default: 1
                             
        """
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'id': id
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(payload):
        """
        create movie
        ---
        tags:
          - movies
        parameters:
            - in: body
              name: body
              description: JSON parameters.
              schema:
                id: movies
                required:
                  - title
                  - release
                properties:
                    title:
                        type: string
                        description: The name of the movie
                        default: Steven Wilson
                    release:
                        type: string
                        description: The release of the movie
                        default: 30
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        movie:
                            type: object
                            properties:
                                id:
                                    type: number
                                    description: The name of the movie
                                    default: 1
                                title:
                                    type: string
                                    description: The name of the movie
                                    default: Steven Wilson
                                release:
                                    type: string
                                    description: The release of the movie
                                    default: 30
        """
        data = request.get_json()
        if data.get('title') is None or data.get('release') is None:
            abort(400)
        movie = Movie(title=data.get('title'), release=data.get('release'))
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(payload, id):
        """
        update movie
        ---
        tags:
          - movies
        parameters:
            - in: path
              name: id
              type: string
              required: True  
            - in: body
              name: body
              description: JSON parameters.
              schema:
                id: movies
                required:
                  - title
                  - release
                properties:
                    title:
                        type: string
                        description: The name of the movie
                        default: Steven Wilson
                    release:
                        type: string
                        description: The release of the movie
                        default: 30
        responses:
            401:
                description: Unathorized
            400:
                description: bad request
            200:
                description: OK
                schema:
                    properties:
                        success:
                            type: boolean
                            default: True
                        movie:
                            type: object
                            properties:
                                id:
                                    type: number
                                    description: The name of the movie
                                    default: 1
                                title:
                                    type: string
                                    description: The name of the movie
                                    default: Steven Wilson
                                release:
                                    type: string
                                    description: The release of the movie
                                    default: 30
        """
        data = request.get_json()
        if data.get('title') is None or data.get('release') is None:
            abort(400)
        movie = Movie.query.get(id)
        if movie == None:
            abort(404)
        movie.title = data.get('title')
        movie.release = data.get('release')
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({'success': False, 'error': 404, 'message': 'resource not found'}),
            404
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({'success': False, 'error': 400, 'message': 'bad request'}),
            400
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({'success': False, 'error': 405, 'message': 'method not alllowed'}),
            405
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({'success': False, 'error': 500, 'message': '500 Internal Server Error'}),
            500
        )

    @app.errorhandler(401)
    def not_athorized(error):
        return (
            jsonify({'success': False, 'error': 401, 'message': 'Unathorized'}),
            401
        )

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
