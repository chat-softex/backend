# app/validators/usuario_validator.py:
from marshmallow import Schema, fields, validate, validates, validates_schema
from app.erros.custom_errors import ValidationError

# Schema de validação de Usuario
class UserSchema(Schema):
    nome = fields.String(
        required=True,
        validate=validate.Length(min=3, max=255),
        error_messages={
            "required": "O nome é obrigatório.",
            "min": "O nome deve ter pelo menos 3 caracteres.",
            "max": "O nome deve ter no máximo 255 caracteres."
        }
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=255),
        error_messages={
            "required": "O email é obrigatório.",
            "invalid": "O email deve ser válido.",
            "max": "O email deve ter no máximo 255 caracteres."
        }
    )
    senha = fields.String(
        required=True,
        validate=[
            validate.Length(min=6, max=10),
            validate.Regexp(
                r'^(?=.*[A-Za-z]{2,})(?=.*\d{2,})(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$',
                error=(
                    "A senha deve ter entre 6 e 10 caracteres, contendo pelo menos duas letras, "
                    "dois números e um caractere especial."
                )
            )
        ],
        error_messages={
            "required": "A senha é obrigatória.",
            "min": "A senha deve ter pelo menos 6 caracteres.",
            "max": "A senha deve ter no máximo 10 caracteres."
        }
    )
    tipo = fields.String(
        required=True,
        validate=validate.OneOf(['avaliador', 'administrador'], error="O tipo deve ser 'avaliador' ou 'administrador'."),
        error_messages={
            "required": "O tipo é obrigatório.",
            "one_of": "O tipo deve ser 'avaliador' ou 'administrador'."
        }
    )

    @validates_schema
    def validate_dependencies(self, data, **kwargs):
        """Validações adicionais, caso sejam necessárias."""
        if data.get("email") and data.get("email").endswith("@exemplo.com"):
            raise ValidationError(
                field="email",
                message="Endereços de email '@exemplo.com' não são permitidos."
            )
