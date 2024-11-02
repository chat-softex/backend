from marshmallow import Schema, fields, validate, ValidationError
from app.repositories.empresa_repository import EmpresaRepository

# Schema de validação de Empresa
class EmpresaSchema(Schema):
    nome_fantasia = fields.String(
        required=True, validate=validate.Length(min=1, max=50)
    )
    cnpj = fields.String(
        required=True, validate=validate.Length(min=14, max=14), validate=validate.Regexp(r'^[0-9]{14}$')
    )
    email = fields.Email(required=True, validate=validate.Length(max=255))
class EmpresaService:

    # Converte os campos nome_fantasia, email para letras minúsculas.
    def _normalize_data(self, data):
        if 'nome_fantasia' in data:
            data['nome_fantasia'] = data['nome_fantasia'].lower()
        if 'email' in data:
            data['email'] = data['email'].lower()
        return data

    # Retorna todos as empresas cadastrados.
    def get_all(self):
        return EmpresaRepository.get_all()

    # Retorna uma empresa pelo ID.
    def get_by_id(self, id):
        empresa = EmpresaRepository.get_by_id(id)
        if not empresa:
            raise Exception("Empresa não encontrada.")
        return empresa
    
    #Retorna a empresa pelo nome fantasia
    def get_by_nome_fantasia(self, nome_fantasia):
        empresa = self.get_by_nome_fantasia(nome_fantasia.lower())
        if not empresa:
            raise Exception("Empresa não encontrada.")
        return empresa
    
    #Retorna a empresa pelo CNPJ
    def get_by_cnpj(self, cnpj):
        empresa = EmpresaRepository.get_by_cnpj(cnpj)
        if not empresa:
            raise Exception("Empresa não encontrada.")
        return empresa
    
    # Retorna uma empresa pelo e-mail.
    def get_by_email_empresa(self, email):
        empresa = EmpresaRepository.get_by_email_empresa(email.lower())
        if not empresa:
            raise Exception("Empresa não encontrada.")
        return empresa

    # Cria uma nova Empresa, garantindo CNPJ e e-mail único.
    def create_empresa(self, data):
        try:
            # Normaliza os dados para letras minúsculas
            normalized_data = self._normalize_data(data)

            # Verifica se o e-mail ou CNPJ já está cadastrado
            if EmpresaRepository.get_by_cnpj(normalized_data['cnpj']):
                raise Exception("CNPJ já está cadastrado.")
            if EmpresaRepository.get_by_email_empresa(normalized_data['email']):
                raise Exception("E-mail já está cadastrado.")

            empresa_data = EmpresaSchema().load(normalized_data)

            return EmpresaRepository.create(empresa_data)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Atualiza os dados de uma empresa, garantindo CNPJ e e-mail único.
    def update(self, id, data):
        empresa = EmpresaRepository.get_by_id(id)
        if not empresa:
            raise Exception("Empresa não encontrada.")

        try:
            # Normaliza os dados para letras minúsculas
            normalized_data = self._normalize_data(data)
            
            # Se o cnpj está sendo alterado, verifica se já está em uso por outra empresa
            if 'cnpj' in normalized_data and normalized_data['cnpj'] != empresa.cnpj:
                if EmpresaRepository.get_by_cnpj(normalized_data['cnpj']):
                    raise Exception("CNPJ já está cadastrado.")
                
            # Se o e-mail está sendo alterado, verifica se já está em uso por outra empresa
            if 'email' in normalized_data and normalized_data['email'] != empresa.email:
                if EmpresaRepository.get_by_email_empresa(normalized_data['email']):
                    raise Exception("E-mail já está cadastrado.")

            updated_data = EmpresaSchema().load(normalized_data, partial=True)

            # Atualiza os atributos da empresa
            for key, value in updated_data.items():
                setattr(empresa, key, value)

            return EmpresaRepository.update(empresa)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Deleta um empresa pelo ID.
    def delete(self, id):
        empresa = EmpresaRepository.get_by_id(id)
        if not empresa:
            raise Exception("Empresa não encontrada.")
        EmpresaRepository.delete(id)
        return {"message": "Empresa deletada com sucesso."}
