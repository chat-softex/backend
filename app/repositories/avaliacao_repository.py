# app/repositories/avaliacao_repository.py
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload
from app.models.avaliacao_model import Avaliacao
from app.models.projeto_model import Projeto
from app import db
from app.erros.custom_errors import NotFoundError, InternalServerError, ConflictError

# Configuração do logger
logger = logging.getLogger("AvaliacaoRepository")

class AvaliacaoRepository:
    """Repositório para operações CRUD com a entidade Avaliacao"""

    # Retorna todas as avaliações com o projeto associado e seu avaliador.
    @staticmethod
    def get_all():
        try:
            avaliacoes = db.session.query(Avaliacao).options(
                joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
            ).all()
            logger.info("Avaliações obtidas com sucesso.")
            return avaliacoes
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todas as avaliações: {e}")
            raise InternalServerError(message="Erro ao buscar avaliações.")

    # Retorna uma avaliação específica pelo ID com o projeto e o avaliador associados.
    @staticmethod
    def get_by_id(id):
        try:
            avaliacao = db.session.query(Avaliacao).filter_by(id=id).options(
                joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
            ).first()
            if not avaliacao:
                logger.warning(f"Avaliação com ID {id} não encontrada.")
                raise NotFoundError(resource="Avaliação", message="Avaliação não encontrada.")
            logger.info(f"Avaliação com ID {id} encontrada com sucesso.")
            return avaliacao
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar avaliação com ID {id}: {e}")
            raise InternalServerError(message="Erro ao buscar avaliação pelo ID.")

    # Adiciona uma nova avaliação ao banco de dados.
    @staticmethod
    def create(avaliacao):
        try:
            db.session.add(avaliacao)
            db.session.commit()
            logger.info(f"Avaliação criada com sucesso: {avaliacao.id}")
            return avaliacao
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Erro de integridade ao criar avaliação: {e}")
            raise ConflictError(resource="Avaliação", message="Conflito ao criar avaliação.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao criar avaliação: {e}")
            raise InternalServerError(message="Erro ao criar avaliação.")

    # Atualiza uma avaliação existente no banco de dados.
    @staticmethod
    def update(avaliacao):
        try:
            db.session.commit()
            logger.info(f"Avaliação com ID {avaliacao.id} atualizada com sucesso.")
            return avaliacao
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar avaliação com ID {avaliacao.id}: {e}")
            raise InternalServerError(message="Erro ao atualizar avaliação.")

    # Remove uma avaliação do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        try:
            avaliacao = AvaliacaoRepository.get_by_id(id)  # Garante que a avaliação existe
            db.session.delete(avaliacao)
            db.session.commit()
            logger.info(f"Avaliação com ID {id} deletada com sucesso.")
        except NotFoundError as e:
            logger.warning(f"Tentativa de deletar avaliação não encontrada: ID {id}")
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar avaliação com ID {id}: {e}")
            raise InternalServerError(message="Erro ao deletar avaliação.")