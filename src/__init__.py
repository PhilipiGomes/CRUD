from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# Instancias
db = SQLAlchemy()
login_manager = LoginManager()
migrate = None


def create_app():
    app = Flask(__name__)
    app.config.from_object("connection")

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

    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()

    return app


# Cria a aplicação
app = create_app()
