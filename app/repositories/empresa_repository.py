# app/repositories/empresa_repository.py
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.empresa_model import Company
from app import db
from app.erros.custom_errors import NotFoundError, InternalServerError, ConflictError

# Configuração do logger
logger = logging.getLogger("CompanyRepository")

class CompanyRepository:
    """Repositório para operações CRUD com a entidade Empresa"""

    # Retorna todas as empresas cadastradas no banco de dados.
    @staticmethod
    def get_all():
        try:
            empresas = Company.query.all()
            logger.info("Empresas obtidas com sucesso.")
            return empresas
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todas as empresas: {e}")
            raise InternalServerError(message="Erro ao buscar empresas.")

    # Retorna a empresa específica pelo ID.
    @staticmethod
    def get_by_id(id):
        try:
            empresa = Company.query.get(id)
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
            empresa = Company.query.filter_by(cnpj=cnpj).first()
            if not empresa:
                logger.warning(f"Empresa com CNPJ '{cnpj}' não encontrada.")
                return None  # retorna None ao invés de levantar NotFoundError
            logger.info(f"Empresa com CNPJ '{cnpj}' encontrada com sucesso.")
            return empresa
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empresa com CNPJ '{cnpj}': {e}")
            raise InternalServerError(message="Erro ao buscar empresa pelo CNPJ.")
        

    @staticmethod
    def get_by_email(email):
        try:
            empresa = Company.query.filter_by(email=email).first()
            if not empresa:
                logger.info(f"Empresa com email {email} não encontrado.")
                return None  # retorna None ao invés de levantar NotFoundError
            logger.info(f"Empresa com email {email} encontrado com sucesso.")
            return empresa
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empresa com email {email}: {e}")
            raise InternalServerError(message="Erro ao buscar empresa pelo email.")    
        
    

    # Adiciona uma nova empresa ao banco de dados.
    @staticmethod
    def create(data):
        try:
            company = Company(**data)
            db.session.add(company)
            db.session.commit()
            logger.info(f"Empresa criada com sucesso: {company.id}")
            return company
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
    def update(company):
        try:
            db.session.commit()
            logger.info(f"Empresa com ID {company.id} atualizada com sucesso.")
            return company
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar empresa com ID {company.id}: {e}")
            raise InternalServerError(message="Erro ao atualizar empresa.")

    # Remove uma empresa do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        try:
            empresa = CompanyRepository.get_by_id(id)
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

