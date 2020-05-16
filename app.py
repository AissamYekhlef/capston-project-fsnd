import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import db_drop_and_create_all,db, setup_db, Movie, Actor, Show
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    # DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    db_drop_and_create_all()


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, PATCH, POST, DELETE, OPTIONS')
        return response


    @app.route('/')
    def home():
        return jsonify({
            'success': True,
            'message': 'hello world'
        })


    @app.route('/actors', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_all_actors(payload):
        try:
            db_drop_and_create_all() 
            return jsonify({
                "success": True,
                "deleted": "All Movies"
            })
        except:
            abort(422)

    @app.route('/movies', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_all_movies(payload):

        try:
            db_drop_and_create_all() 
            return jsonify({
                "success": True,
                "deleted": "All Movies"
            })
        except:
            abort(422)



    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        data = Actor.query.all()
        actors= list(map(Actor.get_actor, data))
        if actors is None or len(actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': actors
        })


    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        data = Movie.query.all()
        movies= list(map(Movie.get_movie, data))
        if movies is None or len(movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': movies
        })


    # @app.route('/movies/<int:movie_id>/actors')
    # def get_movies():
    #     data = Movie.query.all()
    #     movies= list(map(Movie.get_movie, data))
    #     if movies is None or len(movies) == 0:
    #         abort(404)
    #     return jsonify({
    #         'success': True,
    #         'movies': movies
    #     })   

    @app.route('/shows')
    def get_all_shows():
        data = Show.query.all()
        shows= list(map(Show.get_show, data))
        if shows is None or len(shows) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'shows': shows
        })

    @app.route('/shows', methods=['POST'])
    def post_new_show():
        body = request.get_json()
        if body is None:
            abort(404)
        actor_id = body.get('actor_id', None)
        movie_id = body.get('movie_id', None)
     
        try:
          new_show = Show(actor_id=actor_id, movie_id=movie_id)
          new_show.insert()
          return jsonify({
              'success': True,
              'new show': [new_show.get_show()]
          })
        
        except:
            abort(422) 

    @app.route('/actors/<int:actor_id>/movies')
    def get_movies_of_an_actor(actor_id):
        data = Show.query.filter(Show.actor_id == actor_id).all()
        data =  db.session.execute('select movie_id from shows where actor_id='+ str(actor_id)).fetchall()
        
        for d in data:
          movies= Movie.query.get(d.movie_id)
          #  movies= list(map(Movie.get_movie, Movie.query.get(d.)))
          print(movies)
        if movies is None or len(movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': movies
        })        


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
          new_actor = Actor(name=name, age=age, gender=gender)
          new_actor.insert()
          return jsonify({
              'success': True,
              'actors': [new_actor.get_actor()]
          })
        
        except:
            abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        body = request.get_json()
        if 'title' not in body :
            abort(404)
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
            return jsonify({
                'success': True,
                'movies': [new_movie.get_movie()]
            })
        except:
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload,actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()  
        if body is None:
            abort(404)
            
        updated_name = body.get('name', None)
        updated_age = body.get('age', None)
        updated_gender = body.get('gender', None)

        if updated_name is not None:
            actor.name = updated_name
        if updated_age is not None:
            actor.age = updated_age     
        if updated_gender is not None:
            actor.gender = updated_gender
  
        try:
            actor.update() 
            return jsonify({
                'success': True,
                'actors': [actor.get_actor()]
            })
        except:
            abort(422)


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(404)
            
        updated_title = body.get('title', None)
        updated_release_date = body.get('release_date', None)


        if updated_title is not None:
            movie.title = updated_title
        if updated_release_date is not None:
            movie.release_date = updated_release_date     
  
        try:
            movie.update()  
            return jsonify({
                'success': True,
                'movie': movie.get_movie()
            })
        except:
            abort(422)


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        selected_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if selected_actor is None:
            abort(404)
        try:
            selected_actor.delete()  
            return jsonify({
                "success": True,
                "deleted": actor_id
            })
        except:
            abort(422)

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):

        selected_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if selected_movie is None:
            abort(404)
        try:
            selected_movie.delete() 
            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except:
            abort(422)


    # Error Handling

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
        

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

 
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "code": error.error['code'],
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)