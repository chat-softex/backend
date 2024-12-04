import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload
from app.models.avaliacao_model import Review
from app.models.projeto_model import Project
from app import db
from app.erros.custom_errors import NotFoundError, InternalServerError, ConflictError

logger = logging.getLogger("ReviewRepository")

class ReviewRepository:
    """Repositório para operações CRUD com a entidade Avaliacao"""

    # Retorna todas as avaliações com o projeto associado e seu avaliador.
    @staticmethod
    def get_all():
        try:
            avaliacoes = db.session.query(Review).options(
                joinedload(Review.projeto)
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
            avaliacao = db.session.query(Review).filter_by(id=id).options(
                joinedload(Review.projeto)
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
    def create(data):
        try:
            review = Review(**data)
            db.session.add(review)
            db.session.commit()
            logger.info(f"Avaliação criada com sucesso: {review.id}")
            return review
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
    def update(review):
        try:
            db.session.commit()
            logger.info(f"Avaliação com ID {review.id} atualizada com sucesso.")
            return review
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar avaliação com ID {review.id}: {e}")
            raise InternalServerError(message="Erro ao atualizar avaliação.")

    # Remove uma avaliação do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        try:
            avaliacao = ReviewRepository.get_by_id(id)  
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
