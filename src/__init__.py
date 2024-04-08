from flask import Flask, redirect, jsonify
import os 
from .auth import auth
from .bookmarks import bookmarks
from .database import db, Bookmark
from flask_jwt_extended import JWTManager # type: ignore
from src.constants.http_status_codes import *

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('dev'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DB_URI'),
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)
    db.app=app
    db.init_app(app)
    
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()
        
        if bookmark:
            bookmark.visits=bookmark.visits+1
            db.session.commit()
            
            return redirect(bookmark.url)
    
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error': 'Not found'
        }), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error': 'Something went wrong we are working on it'
        }), HTTP_404_NOT_FOUND
    
    
    return app

