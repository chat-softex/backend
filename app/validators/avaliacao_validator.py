# app/validators/avaliacao_validator.py:
from marshmallow import Schema, fields, validate, validates, validates_schema
from app.erros.custom_errors import ValidationError

# Schema de validação de Avaliação
class ReviewSchema(Schema):
    """Schema de validação para Avaliações."""
    projeto_id = fields.Str(
        required=True,
        error_messages={
            "required": "O ID do projeto é obrigatório.",
            "invalid": "O ID do projeto deve ser um UUID válido."
        }
    )
    feedback_qualitativo = fields.String(
        required=True,
        validate=validate.Length(min=10),
        error_messages={
            "required": "O feedback qualitativo é obrigatório.",
            "min": "O feedback deve ter pelo menos 10 caracteres."
        }
    )

    # @validates_schema
    # def validate_dependencies(self, data, **kwargs):
    #     """Validações adicionais entre campos."""
    #     if "feedback_qualitativo" in data and len(data["feedback_qualitativo"].split()) < 3:
    #         raise ValidationError(
    #             field="feedback_qualitativo",
    #             message="O feedback qualitativo deve conter pelo menos 3 palavras."
    #         )




