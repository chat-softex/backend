# app/validators/avaliacao_validator.py:
from marshmallow import Schema, fields, validate, ValidationError, validates

# Schema de validação de Avaliacao
class ReviewSchema(Schema):
    """Schema de validação para Avaliações."""
    projeto_id = fields.UUID(required=True)
    feedback_qualitativo = fields.String(
        required=True, validate=validate.Length(min=10)
    )