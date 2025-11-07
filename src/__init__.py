import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Carregar variáveis de ambiente
load_dotenv()

# Instâncias
db = SQLAlchemy()
login_manager = LoginManager()
migrate = None


def create_app():
    app = Flask(__name__)

    # Configura o app com as variáveis de ambiente
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),  # Definindo a chave secreta
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "SQLALCHEMY_DATABASE_URI"
        ),  # Usando a URI configurada na .env
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Desativando modificações de rastreamento
    )

    # Inicializa as extensões com o app
    db.init_app(app)
    login_manager.init_app(app)

    global migrate
    migrate = Migrate(app, db)

    # Configura o login_manager
    login_manager.blueprint_login_views = {"usuarios": "usuarios.login"}
    login_manager.login_message = "Por favor, faça login para acessar esta página."

    # Função para carregar o usuário pelo ID (necessário para o flask-login)
    @login_manager.user_loader
    def load_user(user_id):
        from src.models.usuario_model import UsuarioModel

        return UsuarioModel.query.get(int(user_id))

    # Registra os blueprints
    from src.view.usuario_view import bp_usuarios

    app.register_blueprint(bp_usuarios)

    # Cria as tabelas do banco de dados (cuidado, essa operação cria tudo automaticamente, pode ser perigoso em produção)
    # By default we SKIP automatic creation on app startup in production/deploy
    # This avoids attempts to connect to a DB during deploy (e.g. Render) when
    # the DB isn't ready or credentials are provided via environment vars.
    # To enable automatic creation (dev only), set SKIP_DB_CREATE=0 in the env.
    skip_db_create = os.getenv("SKIP_DB_CREATE", "1")
    if skip_db_create != "1":
        with app.app_context():
            db.create_all()

    return app


# Cria a aplicação
app = create_app()
