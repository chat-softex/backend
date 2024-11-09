# app/repositories/projeto_repository.py:
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload
from app.models.projeto_model import Projeto
from app import db
from app.erros.custom_errors import NotFoundError, InternalServerError, ConflictError

# Configuração do logger
logger = logging.getLogger("ProjetoRepository")

class ProjetoRepository:
    """Repositório para operações CRUD com a entidade Projeto"""

    # Retorna todos os projetos com seus relacionamentos de avaliador, empresa e avaliação.
    @staticmethod
    def get_all():
        try:
            projetos = db.session.query(Projeto).options(
                joinedload(Projeto.avaliador),  # Carrega o avaliador relacionado
                joinedload(Projeto.empresa),    # Carrega a empresa relacionada
                joinedload(Projeto.avaliacao)   # Carrega a avaliação relacionada (1:1)
            ).all()
            logger.info("Projetos obtidos com sucesso.")
            return projetos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todos os projetos: {e}")
            raise InternalServerError(message="Erro ao buscar projetos.")

    # Retorna um projeto específico pelo ID com seus relacionamentos.
    @staticmethod
    def get_by_id(id):
        try:
            projeto = db.session.query(Projeto).filter_by(id=id).options(
                joinedload(Projeto.avaliador),
                joinedload(Projeto.empresa),
                joinedload(Projeto.avaliacao)
            ).first()
            if not projeto:
                logger.warning(f"Projeto com ID {id} não encontrado.")
                raise NotFoundError(resource="Projeto", message="Projeto não encontrado.")
            logger.info(f"Projeto com ID {id} encontrado com sucesso.")
            return projeto
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar projeto com ID {id}: {e}")
            raise InternalServerError(message="Erro ao buscar projeto pelo ID.")

    # Adiciona um novo projeto ao banco de dados.
    @staticmethod
    def create(projeto):
        try:
            db.session.add(projeto)
            db.session.commit()
            logger.info(f"Projeto criado com sucesso: {projeto.id}")
            return projeto
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Erro de integridade ao criar projeto: {e}")
            raise ConflictError(resource="Projeto", message="Conflito ao criar projeto.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao criar projeto: {e}")
            raise InternalServerError(message="Erro ao criar projeto.")

    # Atualiza um projeto existente no banco de dados.
    @staticmethod
    def update(projeto):
        try:
            db.session.commit()
            logger.info(f"Projeto com ID {projeto.id} atualizado com sucesso.")
            return projeto
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar projeto com ID {projeto.id}: {e}")
            raise InternalServerError(message="Erro ao atualizar projeto.")

    # Remove um projeto do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        try:
            projeto = ProjetoRepository.get_by_id(id)  # Garante que o projeto existe
            db.session.delete(projeto)
            db.session.commit()
            logger.info(f"Projeto com ID {id} deletado com sucesso.")
        except NotFoundError as e:
            logger.warning(f"Tentativa de deletar projeto não encontrado: ID {id}")
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar projeto com ID {id}: {e}")
            raise InternalServerError(message="Erro ao deletar projeto.")
