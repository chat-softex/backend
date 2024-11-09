# app/validators/empresa_validator.py:
from marshmallow import Schema, fields, validate, ValidationError, validates
from validate_docbr import CNPJ

# Schema de validação de Empresa
class EmpresaSchema(Schema):
    """Schema de validação para Empresas."""
    nome_fantasia = fields.String(
        required=True,
        validate=validate.Length(min=3, max=255)
    )
    cnpj = fields.String(
        required=True,
        validate=validate.Length(equal=18)  # Formato esperado: XX.XXX.XXX/XXXX-XX
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=255)
    )

    @validates("cnpj")
    def _validate_cnpj(self, cnpj):
        """Valida se o CNPJ está no formato correto e é válido."""
        cnpj_validator = CNPJ()
        if not cnpj_validator.validate(cnpj):
            raise ValidationError("CNPJ inválido. Certifique-se de que o CNPJ está no formato XX.XXX.XXX/XXXX-XX e é válido.")

