# app/repositories/empresa_repository.py
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.empresa_model import Empresa
from app import db
from app.erros.custom_errors import NotFoundError, InternalServerError, ConflictError

# Configuração do logger
logger = logging.getLogger("EmpresaRepository")

class EmpresaRepository:
    """Repositório para operações CRUD com a entidade Empresa"""

    # Retorna todas as empresas cadastradas no banco de dados.
    @staticmethod
    def get_all():
        try:
            empresas = Empresa.query.all()
            logger.info("Empresas obtidas com sucesso.")
            return empresas
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todas as empresas: {e}")
            raise InternalServerError(message="Erro ao buscar empresas.")

    # Retorna a empresa específica pelo ID.
    @staticmethod
    def get_by_id(id):
        try:
            empresa = Empresa.query.get(id)
            if not empresa:
                logger.warning(f"Empresa com ID {id} não encontrada.")
                raise NotFoundError(resource="Empresa", message="Empresa não encontrada.")
            logger.info(f"Empresa com ID {id} encontrada com sucesso.")
            return empresa
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empresa com ID {id}: {e}")
            raise InternalServerError(message="Erro ao buscar empresa pelo ID.")
    

    # Retorna a empresa específica pelo CNPJ.
    @staticmethod
    def get_by_cnpj(cnpj):
        try:
            empresa = Empresa.query.filter_by(cnpj=cnpj).first()
            if not empresa:
                logger.warning(f"Empresa com CNPJ '{cnpj}' não encontrada.")
                raise NotFoundError(resource="Empresa", message="Empresa com esse CNPJ não encontrada.")
            logger.info(f"Empresa com CNPJ '{cnpj}' encontrada com sucesso.")
            return empresa
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empresa com CNPJ '{cnpj}': {e}")
            raise InternalServerError(message="Erro ao buscar empresa pelo CNPJ.")
    

    # Adiciona uma nova empresa ao banco de dados.
    @staticmethod
    def create(empresa):
        try:
            db.session.add(empresa)
            db.session.commit()
            logger.info(f"Empresa criada com sucesso: {empresa.id}")
            return empresa
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Erro de integridade ao criar empresa: {e}")
            raise ConflictError(resource="Empresa", message="CNPJ já cadastrado.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao criar empresa: {e}")
            raise InternalServerError(message="Erro ao criar empresa.")

    # Atualiza uma empresa existente no banco de dados.
    @staticmethod
    def update(empresa):
        try:
            db.session.commit()
            logger.info(f"Empresa com ID {empresa.id} atualizada com sucesso.")
            return empresa
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar empresa com ID {empresa.id}: {e}")
            raise InternalServerError(message="Erro ao atualizar empresa.")

    # Remove uma empresa do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        try:
            empresa = EmpresaRepository.get_by_id(id)
            db.session.delete(empresa)
            db.session.commit()
            logger.info(f"Empresa com ID {id} deletada com sucesso.")
        except NotFoundError as e:
            logger.warning(f"Tentativa de deletar empresa não encontrada: ID {id}")
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar empresa com ID {id}: {e}")
            raise InternalServerError(message="Erro ao deletar empresa.")