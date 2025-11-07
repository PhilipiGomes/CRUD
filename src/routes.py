from typing import Any, Dict

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from marshmallow import ValidationError

from src.models.usuario_model import UsuarioModel
from src.schemas.usuario_schema import LoginSchema, UsuarioSchema
from src.services.usuario_service import (
    cadastrar_usuario,
    editar_usuario,
    excluir_usuario,
)

bp_usuarios = Blueprint("usuarios", __name__)
usuario_schema = UsuarioSchema()
login_schema = LoginSchema()


@bp_usuarios.get("/")
def index():
    if current_user.is_authenticated:
        # Redirect authenticated users to the HTML users page (not the JSON API)
        return redirect(url_for("usuarios.usuarios_page"))
    return redirect(url_for("usuarios.login_page"))


@bp_usuarios.get("/login")
def login_page():
    return render_template("login.html")


@bp_usuarios.get("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")


@bp_usuarios.get("/usuarios/list")
@login_required
def usuarios_page():
    usuarios = UsuarioModel.query.all()
    return render_template("usuarios.html", usuarios=usuarios)


@bp_usuarios.post("/cadastro")
def cadastro():
    """Rota para cadastro de usuário"""
    try:
        if not request.is_json:
            return jsonify({"message": "Dados inválidos!"}), 400

        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "Dados inválidos!"}), 400

        # Validação dos dados recebidos
        try:
            if not isinstance(json_data, dict):
                return (
                    jsonify({"message": "Dados inválidos! Esperado um objeto JSON."}),
                    400,
                )
            schema_data = usuario_schema.load(json_data)
            dados: Dict[str, Any] = dict(schema_data) if schema_data else {}
        except ValidationError as err:
            return jsonify({"message": "Dados inválidos!", "errors": err.messages}), 400

        # Verifica se já existe usuário com este email
        email = dados.get("email")
        if email and UsuarioModel.query.filter_by(email=email).first():
            return jsonify({"message": "Email já cadastrado!"}), 400

        # Cadastra o usuário
        usuario = cadastrar_usuario(
            nome=dados["nome"], email=dados["email"], senha=dados["senha"]
        )

        # Retorna os dados do usuário cadastrado
        return (
            jsonify(
                {
                    "message": "Usuário cadastrado com sucesso!",
                    "usuario": usuario_schema.dump(usuario),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"message": "Erro ao cadastrar usuário", "error": str(e)}), 500


@bp_usuarios.post("/login")
def login():
    """Rota para login de usuário"""
    try:
        if not request.is_json:
            return jsonify({"message": "Dados inválidos!"}), 400

        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "Dados inválidos!"}), 400

        # Validação dos dados recebidos
        try:
            if not isinstance(json_data, dict):
                return (
                    jsonify({"message": "Dados inválidos! Esperado um objeto JSON."}),
                    400,
                )
            schema_data = login_schema.load(json_data)
            dados: Dict[str, Any] = dict(schema_data) if schema_data else {}
        # trunk-ignore(ruff/E722)
        except:
            return jsonify({"message": "Um erro ocorreu."}), 400

        # Busca o usuário pelo email
        email = dados.get("email")
        if not email:
            return jsonify({"message": "Email é obrigatório!"}), 400

        usuario = UsuarioModel.query.filter_by(email=email).first()

        # Verifica se o usuário existe e se a senha está correta
        senha = dados.get("senha")
        if not usuario or not senha or not usuario.verificar_senha(senha):
            return jsonify({"message": "Email ou senha inválidos!"}), 400

        # Realiza o login
        login_user(usuario)

        return (
            jsonify(
                {
                    "message": "Login realizado com sucesso!",
                    "usuario": usuario_schema.dump(usuario),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"message": "Erro ao realizar login", "error": str(e)}), 500


@bp_usuarios.post("/logout")
@login_required
def logout():
    """Rota para logout de usuário"""
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200


@bp_usuarios.get("/usuarios")
@login_required
def listar():
    """Rota para listar todos os usuários"""
    try:
        usuarios = UsuarioModel.query.all()
        return jsonify({"usuarios": usuario_schema.dump(usuarios, many=True)}), 200

    except Exception as e:
        return jsonify({"message": "Erro ao listar usuários", "error": str(e)}), 500


@bp_usuarios.get("/usuarios/<int:id>")
@login_required
def detalhar(id):
    """Rota para detalhar um usuário específico"""
    try:
        usuario = UsuarioModel.query.get_or_404(id)
        return jsonify(usuario_schema.dump(usuario)), 200

    except Exception as e:
        return jsonify({"message": "Erro ao detalhar usuário", "error": str(e)}), 500


@bp_usuarios.put("/usuarios/<int:id>")
@login_required
def atualizar(id):
    """Rota para atualizar um usuário"""
    try:
        if not request.is_json:
            return jsonify({"message": "Dados inválidos!"}), 400

        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "Dados inválidos!"}), 400

        # Verifica se o usuário existe
        usuario = UsuarioModel.query.get_or_404(id)

        # Apenas o próprio usuário pode editar seus dados
        if usuario.id != current_user.id:
            return jsonify({"message": "Não autorizado!"}), 403

        # Validação dos dados recebidos (partial=True permite updates parciais)
        try:
            if not isinstance(json_data, dict):
                return (
                    jsonify({"message": "Dados inválidos! Esperado um objeto JSON."}),
                    400,
                )
            schema_data = usuario_schema.load(json_data, partial=True)
            dados: Dict[str, Any] = dict(schema_data) if schema_data else {}
        except ValidationError as err:
            return jsonify({"message": "Dados inválidos!", "errors": err.messages}), 400

        # Se for alterar o email, verifica se já existe
        novo_email = dados.get("email")
        if novo_email and novo_email != usuario.email:
            if UsuarioModel.query.filter_by(email=novo_email).first():
                return jsonify({"message": "Email já cadastrado!"}), 400

        # Atualiza o usuário
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")

        return editar_usuario(usuario, nome=nome, email=email, senha=senha)

    except Exception as e:
        return jsonify({"message": "Erro ao atualizar usuário", "error": str(e)}), 500


@bp_usuarios.delete("/usuarios/<int:id>")
@login_required
def deletar(id):
    """Rota para deletar um usuário"""
    try:
        # Verifica se o usuário existe
        usuario = UsuarioModel.query.get_or_404(id)

        # Deleta o usuário
        return excluir_usuario(usuario)

    except Exception as e:
        return jsonify({"message": "Erro ao deletar usuário", "error": str(e)}), 500
