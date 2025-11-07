from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from src import db
from src.models.usuario_model import UsuarioModel


def cadastrar_usuario(nome, email, senha) -> UsuarioModel:
    usuario_db = UsuarioModel()
    usuario_db.nome = nome
    usuario_db.email = email
    usuario_db.gen_senha(senha)
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db


def editar_usuario(usuario, nome=None, email=None, senha=None):
    """Edita os dados do usuário, permitindo a atualização de nome, email e senha."""
    try:
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha:
            usuario.senha = usuario.gen_senha(senha)

        db.session.commit()

        return jsonify({"message": "Usuário atualizado com sucesso!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "message": "Erro ao atualizar o usuário no banco de dados.",
                    "error": str(e),
                }
            ),
            500,
        )

    except Exception as e:
        return (
            jsonify(
                {"message": "Erro inesperado ao editar o usuário.", "error": str(e)}
            ),
            500,
        )


def excluir_usuario(usuario):
    """Exclui um usuário do banco de dados."""
    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuário excluído com sucesso!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "message": "Erro ao excluir o usuário no banco de dados.",
                    "error": str(e),
                }
            ),
            500,
        )

    except Exception as e:
        return (
            jsonify(
                {"message": "Erro inesperado ao excluir o usuário.", "error": str(e)}
            ),
            500,
        )
