from src import app
from src.models.usuario_model import UsuarioModel


def inspect(email: str | None = None):
    with app.app_context():
        if email:
            u = UsuarioModel.query.filter_by(email=email).first()
            if not u:
                print(f"No user found with email={email}")
                return
            print(
                f"id={u.id} nome={u.nome} email={u.email} senha(len)={len(u.senha) if u.senha else 0}"
            )
            print(f"senha value: {u.senha}")
        else:
            users = UsuarioModel.query.all()
            for u in users:
                print(
                    f"id={u.id} nome={u.nome} email={u.email} senha(len)={len(u.senha) if u.senha else 0}"
                )


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else None
    inspect(email)
