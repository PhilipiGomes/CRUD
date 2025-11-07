from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import db


class UsuarioModel(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # Password hashes produced by Werkzeug are longer than 50 chars.
    # Use a larger column to avoid truncation which makes verification fail.
    senha = db.Column(db.String(255), nullable=False)

    # Gera o hash da senha e armazena no campo 'senha'
    def gen_senha(self, senha):
        self.senha = generate_password_hash(senha)

    # Verifica se a senha informada corresponde ao hash armazenado
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
