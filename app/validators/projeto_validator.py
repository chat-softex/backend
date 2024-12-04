from marshmallow import Schema, fields, validate, validates, validates_schema
from app.erros.custom_errors import ValidationError

class ProjectSchema(Schema):
    titulo_projeto = fields.String(
        required=True, 
        validate=validate.Length(min=5, max=255),
        error_messages={
            "required": "O título do projeto é obrigatório.",
            "min": "O título deve ter pelo menos 5 caracteres.",
            "max": "O título deve ter no máximo 255 caracteres."
        }
    )
    status = fields.String(
        required=True,
        validate=validate.OneOf(['em avaliação', 'aprovado', 'reprovado']),
        error_messages={
            "required": "O status é obrigatório.",
            "one_of": "O status deve ser 'em avaliação', 'aprovado' ou 'reprovado'."
        }
    )
    arquivo = fields.String(
        required=True,
        validate=validate.Regexp(
            r".*\.(pdf|doc|docx)$",
            error="O arquivo deve ter a extensão .pdf, .doc ou .docx."
        ),
        error_messages={"required": "O arquivo é obrigatório."}
    )
    avaliador_id = fields.UUID(
        required=True,
        error_messages={"required": "O ID do avaliador é obrigatório."}
    )
    empresa_id = fields.UUID(
        required=True,
        error_messages={"required": "O ID da empresa é obrigatório."}
    )

    # @validates_schema
    # def validate_dependencies(self, data, **kwargs):
    #     """Valida relações entre campos (ex.: IDs de avaliador e empresa)."""
    #     if data.get("avaliador_id") == data.get("empresa_id"):
    #         raise ValidationError(field="avaliador_id/empresa_id", message="Avaliador e empresa não podem ser os mesmos.")

