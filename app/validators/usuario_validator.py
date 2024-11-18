# app/validators/usuario_validator.py:
from marshmallow import Schema, fields, validate, ValidationError

# Schema de validação de Usuario
class UserSchema(Schema):
    nome = fields.String(
        required=True, 
        validate=validate.Length(min=3, max=255)
    )
    email = fields.Email(
        required=True, 
        validate=validate.Length(max=255)
    )
    senha = fields.String(
        required=True,
        validate=[
            validate.Length(min=6, max=10),
            validate.Regexp(
                r'^(?=.*[A-Za-z]{2,})(?=.*\d{2,})(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$',
                error=(
                    "A senha deve ter entre 6 e 10 caracteres, contendo pelo menos duas letras, "
                    "um caractere especial e dois números."
                )
            )
        ]
    )
    tipo = fields.String(
        required=True,
        validate=validate.OneOf(['avaliador', 'administrador'], error="O tipo deve ser 'avaliador' ou 'administrador'.")
    )
