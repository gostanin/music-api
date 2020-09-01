from flask import Flask
from flask_cors import CORS

from music.controllers.songs import songs


def create_app():
    app = Flask(__name__)
    app.config.from_object('music.settings')
    CORS(app, resources={
         r'/*': {'origins': app.config['ALLOWED_CORS_ORIGINS']}})
    app.register_blueprint(songs, url_prefix='/api/v1/songs')

    return app
