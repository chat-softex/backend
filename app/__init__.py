from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config.config import Config

from app.middlewares.cors_middleware import init_cors

db = SQLAlchemy()
migrate = Migrate()  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    init_cors(app)


    # importar model Usuario
    # importar model Avaliacao
    # importar model Projeto

    # from app.routes.usuario_routes import usuario_routes
    # from app.routes.projeto_routes import projeto_routes
    # from app.routes.avaliacao_routes import avaliacao_routes
    # app.register_blueprint(usuario_routes)
    # app.register_blueprint(projeto_routes)
    # app.register_blueprint(avaliacao_routes)

    return app

