import re

from marshmallow import Schema, ValidationError, fields, validates


class UsuarioSchema(Schema):
    id = fields.Integer(dump_only=True)
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(required=True, load_only=True)

    @validates("nome")
    def validate_nome(self, value):
        if len(value) < 3:
            raise ValidationError("O nome deve ter pelo menos 3 caracteres")
        if len(value) > 50:
            raise ValidationError("O nome deve ter no máximo 50 caracteres")

    @validates("senha")
    def validate_senha(self, value):
        if len(value) < 6:
            raise ValidationError("A senha deve ter pelo menos 6 caracteres")
        if len(value) > 50:
            raise ValidationError("A senha deve ter no máximo 50 caracteres")
        if not re.search(r"[A-Z]", value):
            raise ValidationError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r"[a-z]", value):
            raise ValidationError("A senha deve conter pelo menos uma letra minúscula")
        if not re.search(r"[0-9]", value):
            raise ValidationError("A senha deve conter pelo menos um número")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    senha = fields.Str(required=True)
