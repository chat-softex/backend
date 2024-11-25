# app/service/empresa_service.py:
import logging
import marshmallow
from app.repositories.empresa_repository import CompanyRepository 
from app.validators.empresa_validator import CompanySchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError, ValidationError
from validate_docbr import CNPJ as CNPJValidator
from app.erros.error_handler import ErrorHandler

# Configuração do logger
logger = logging.getLogger(__name__)

class CompanyService:
    def __init__(self):
        self.schema = CompanySchema()

    def _normalize_data(self, data):
        """Converte campos de string para letras minúsculas."""
        if 'nome_fantasia' in data:
            data['nome_fantasia'] = data['nome_fantasia'].lower()
        if 'email' in data:
            data['email'] = data['email'].lower()
        if 'cnpj' in data:
            cnpj_validator = CNPJValidator()
            data['cnpj'] = cnpj_validator.mask(data['cnpj'])    
        return data

    def get_all(self):
        """Retorna todas as empresas cadastradas."""
        try:
            empresas = CompanyRepository.get_all()
            logger.info("Empresas obtidas com sucesso.")
            return empresas
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar empresas: {e}")
            raise InternalServerError("Erro inesperado ao buscar empresas.")

    def get_by_id(self, company_id):
        """Busca uma empresa específica pelo ID."""
        try:
            if not company_id or not isinstance(company_id, str):
                raise ValidationError(field="company_id", message="ID inválido.")

            empresa = CompanyRepository.get_by_id(company_id)
            if not empresa:
                logger.warning(f"Empresa com ID {company_id} não encontrada.")
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")
            
            logger.info(f"Empresa com ID {company_id} encontrada com sucesso.")
            return empresa
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar empresa {company_id}: {e}")
            raise InternalServerError("Erro inesperado ao buscar empresa.")

    def create(self, data):
        """Cria uma nova empresa, garantindo que o CNPJ e e-mail sejam únicos."""
        try:
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")

            normalized_data = self._normalize_data(data)            

            # verifica se o CNPJ ou e-mail já estão cadastrados
            if CompanyRepository.get_by_cnpj(normalized_data['cnpj']):
                logger.warning(f"CNPJ já cadastrado: {normalized_data['cnpj']}")
                raise ConflictError(resource="Empresa", message="CNPJ já cadastrado.")
            if CompanyRepository.get_by_email(normalized_data['email']):
                logger.warning(f"E-mail já cadastrado: {normalized_data['email']}")
                raise ConflictError(resource="Empresa", message="E-mail já cadastrado.")

            # valida os dados com o schema
            try:
                empresa_data = self.schema.load(normalized_data)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)

            # cria a empresa no banco de dados
            empresa = CompanyRepository.create(empresa_data)
            logger.info(f"Empresa criada com sucesso: ID {empresa.id}")
            return empresa
        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.message}")
            raise
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar empresa: {e}")
            raise InternalServerError("Erro inesperado ao criar empresa.")

    def update(self, company_id, data):
        """Atualiza os dados de uma empresa."""
        try:
            if not company_id or not isinstance(company_id, str):
                raise ValidationError(field="company_id", message="ID inválido.")
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados inválidos para atualização.")
            
            empresa = self.get_by_id(company_id)
            if not empresa:
                logger.warning(f"Empresa com ID {company_id} não encontrada.")
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")

            # normaliza os dados
            updated_data = self._normalize_data(data)

            # se o CNPJ foi alterado, valida e verifica se já está cadastrado
            if 'cnpj' in updated_data and updated_data['cnpj'] != empresa.cnpj:
                if CompanyRepository.get_by_cnpj(updated_data['cnpj']):
                    logger.warning(f"CNPJ já cadastrado: {updated_data['cnpj']}")
                    raise ConflictError(resource="Empresa", message="CNPJ já cadastrado.")

            # se o e-mail foi alterado, verifica se já está cadastrado
            if 'email' in updated_data and updated_data['email'] != empresa.email:
                if CompanyRepository.get_by_email(updated_data['email']):
                    logger.warning(f"E-mail já cadastrado: {updated_data['email']}")
                    raise ConflictError(resource="Empresa", message="E-mail já cadastrado.")

            # valida os dados com o schema
            try:
                updated_data = self.schema.load(updated_data, partial=True)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)    
                

            # atualiza os atributos da empresa
            for key, value in updated_data.items():
                setattr(empresa, key, value)

            # salva a atualização no repositório
            updated_empresa = CompanyRepository.update(empresa)
            logger.info(f"Empresa com ID {company_id} atualizada com sucesso.")
            return updated_empresa
        except NotFoundError as e:
            # repropaga o erro específico para tratamento externo
            logger.warning(f"[NotFoundError] {e}")
            raise
        except ConflictError as e:
            # repropaga conflitos de dados
            logger.warning(f"[ConflictError] {e}")
            raise
        except ValidationError as err:
             # tratamento para erros de validação
            logger.warning(f"[ValidationError] {err.message}")
            raise 
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar empresa {company_id}: {e}")
            raise InternalServerError("Erro inesperado ao atualizar empresa.")


    def delete(self, company_id):
        """Remove uma empresa pelo ID."""
        try:
            if not company_id or not isinstance(company_id, str):
                raise ValidationError(field="company_id", message="ID inválido.")
            
            empresa = CompanyRepository.get_by_id(company_id)
            if not empresa:
                logger.warning(f"Tentativa de deletar empresa com ID {company_id} não encontrada.")
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")
            
            CompanyRepository.delete(company_id)
            logger.info(f"Empresa {company_id} deletada com sucesso.")
            return {"message": "Empresa deletada com sucesso."}
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar empresa {company_id}: {e}")
            raise InternalServerError("Erro inesperado ao deletar empresa.")