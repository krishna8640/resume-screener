from flask import Flask
from flask_cors import CORS
from app.routes import api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Limit upload size (5MB)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    app.register_blueprint(api)

    return app

app = create_app()