# app/validators/projeto_validator.py:
from marshmallow import Schema, fields, validate, ValidationError, validates

# Schema de validação de Projeto
class ProjetoSchema(Schema):
    titulo_projeto = fields.String(
        required=True, 
        validate=validate.Length(min=5)
    )
    status = fields.String(
        required=True,
        validate=validate.OneOf(['em avaliação', 'aprovado', 'reprovado'])
    )
    arquivo = fields.String(required=True)
    avaliador_id = fields.UUID(required=True)
    empresa_id = fields.UUID(required=True)