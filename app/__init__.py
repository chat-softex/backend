from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes import usuario_routes, projeto_routes, avaliacao_routes
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(projeto_routes.bp)
    app.register_blueprint(avaliacao_routes.bp)

    return app