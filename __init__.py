from flask import Flask
from config import Config
from models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
