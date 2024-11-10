# app/service/empresa_service.py:
import logging
from marshmallow import ValidationError
from app.repositories.empresa_repository import EmpresaRepository
from app.validators.empresa_validator import EmpresaSchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError

# Configuração do logger
logger = logging.getLogger(__name__)

class EmpresaService:
    def __init__(self):
        self.schema = EmpresaSchema()

    def _normalize_data(self, data):
        """Converte campos de string para letras minúsculas."""
        if 'nome_fantasia' in data:
            data['nome_fantasia'] = data['nome_fantasia'].lower()
        if 'email' in data:
            data['email'] = data['email'].lower()
        return data

    def get_all(self):
        """Retorna todas as empresas cadastradas."""
        try:
            empresas = EmpresaRepository.get_all()
            logger.info("Empresas obtidas com sucesso.")
            return empresas
        except Exception as e:
            logger.error("Erro ao buscar todas as empresas: %s", e)
            raise InternalServerError("Erro ao buscar todas as empresas.")

    def get_by_id(self, empresa_id):
        """Busca uma empresa específica pelo ID."""
        try:
            empresa = EmpresaRepository.get_by_id(empresa_id)
            if not empresa:
                logger.warning("Empresa com ID %s não encontrada.", empresa_id)
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")
            logger.info("Empresa com ID %s obtida com sucesso.", empresa_id)
            return empresa
        except Exception as e:
            logger.error("Erro ao buscar empresa com ID %s: %s", empresa_id, e)
            raise InternalServerError("Erro ao buscar empresa.")

    def create_empresa(self, data):
        """Cria uma nova empresa, garantindo que o CNPJ e e-mail sejam únicos."""
        try:
            # Normaliza os dados
            empresa_data = self._normalize_data(data)

            # Verifica se o CNPJ ou e-mail já estão cadastrados
            if EmpresaRepository.get_by_cnpj(empresa_data['cnpj']):
                logger.warning("CNPJ já cadastrado: %s", empresa_data['cnpj'])
                raise ConflictError(resource="Empresa", message="CNPJ já cadastrado.")
            if EmpresaRepository.get_by_email_empresa(empresa_data['email']):
                logger.warning("E-mail já cadastrado: %s", empresa_data['email'])
                raise ConflictError(resource="Empresa", message="E-mail já cadastrado.")

            # Valida os dados com o schema
            empresa_data = self.schema.load(empresa_data)

            # Cria a empresa no banco de dados
            empresa = EmpresaRepository.create(empresa_data)
            logger.info("Empresa criada com sucesso: %s", empresa)
            return empresa
        except ValidationError as err:
            logger.warning("Erro na validação dos dados da empresa: %s", err.messages)
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error("Erro ao criar empresa: %s", e)
            raise InternalServerError("Erro ao criar empresa.")

    def update(self, empresa_id, data):
        """Atualiza os dados de uma empresa."""
        try:
            empresa = EmpresaRepository.get_by_id(empresa_id)
            if not empresa:
                logger.warning("Empresa com ID %s não encontrada.", empresa_id)
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")

            # Normaliza os dados
            updated_data = self._normalize_data(data)

            # Se o CNPJ foi alterado, valida e verifica se já está cadastrado
            if 'cnpj' in updated_data and updated_data['cnpj'] != empresa.cnpj:
                if EmpresaRepository.get_by_cnpj(updated_data['cnpj']):
                    logger.warning("CNPJ já cadastrado: %s", updated_data['cnpj'])
                    raise ConflictError(resource="Empresa", message="CNPJ já cadastrado.")

            # Se o e-mail foi alterado, verifica se já está cadastrado
            if 'email' in updated_data and updated_data['email'] != empresa.email:
                if EmpresaRepository.get_by_email_empresa(updated_data['email']):
                    logger.warning("E-mail já cadastrado: %s", updated_data['email'])
                    raise ConflictError(resource="Empresa", message="E-mail já cadastrado.")

            # Valida os dados com o schema
            updated_data = self.schema.load(updated_data, partial=True)

            # Atualiza os atributos da empresa
            for key, value in updated_data.items():
                setattr(empresa, key, value)

            # Salva a atualização no repositório
            empresa = EmpresaRepository.update(empresa)
            logger.info("Empresa com ID %s atualizada com sucesso.", empresa_id)
            return empresa
        except ValidationError as err:
            logger.warning("Erro na validação dos dados da empresa: %s", err.messages)
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error("Erro ao atualizar empresa com ID %s: %s", empresa_id, e)
            raise InternalServerError("Erro ao atualizar empresa.")

    def delete(self, empresa_id):
        """Remove uma empresa pelo ID."""
        try:
            empresa = EmpresaRepository.get_by_id(empresa_id)
            if not empresa:
                logger.warning("Tentativa de deletar empresa não encontrada: ID %s", empresa_id)
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")
            EmpresaRepository.delete(empresa_id)
            logger.info("Empresa com ID %s deletada com sucesso.", empresa_id)
            return {"message": "Empresa deletada com sucesso."}
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Erro ao deletar empresa com ID %s: %s", empresa_id, e)
            raise InternalServerError("Erro ao deletar empresa.")