# app/validators/empresa_validator.py:
from marshmallow import Schema, fields, validate, validates, validates_schema
from app.erros.custom_errors import ValidationError
from validate_docbr import CNPJ

# Schema de validação de Empresa
class CompanySchema(Schema):
    """Schema de validação para Empresas."""
    nome_fantasia = fields.String(
        required=True,
        validate=validate.Length(min=3, max=255),
        error_messages={
            "required": "O nome fantasia é obrigatório.",
            "min": "O nome fantasia deve ter pelo menos 3 caracteres.",
            "max": "O nome fantasia deve ter no máximo 255 caracteres."
        }
    )
    cnpj = fields.String(
        required=True,
        validate=validate.Length(max=18),  # No máximo 18 caracteres, incluindo pontuações
        error_messages={
            "required": "O CNPJ é obrigatório.",
            "max": "O CNPJ deve ter no máximo 18 caracteres, incluindo pontuações."
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

    @validates("cnpj")
    def _validate_cnpj(self, cnpj):
        """Valida se o CNPJ está no formato correto e é válido."""
        cnpj_validator = CNPJ()
        if not cnpj_validator.validate(cnpj):
            raise ValidationError(
                field="cnpj",
                message="CNPJ inválido. Certifique-se de que o CNPJ está no formato XX.XXX.XXX/XXXX-XX e é válido."
            )

    # @validates_schema
    # def validate_dependencies(self, data, **kwargs):
    #     """Validações adicionais, caso sejam necessárias."""
    #     if "email" in data and data["email"].endswith("@exemplo.com"):
    #         raise ValidationError(
    #             field="email",
    #             message="Emails com domínio '@exemplo.com' não são permitidos."
    #         )
