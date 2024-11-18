# app/service/avaliacao_service.py
import logging
from marshmallow import ValidationError
from app.repositories.avaliacao_repository import ReviewRepository
from app.repositories.projeto_repository import ProjectRepository
from app.validators.avaliacao_validator import ReviewSchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError

logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self):
        self.schema = ReviewSchema()

    def get_all(self):
        """Retorna todas as avaliações cadastradas com seus projetos e avaliadores."""
        try:
            avaliacoes = ReviewRepository.get_all()
            logger.info("Avaliações obtidas com sucesso.")
            return avaliacoes
        except Exception as e:
            logger.error(f"Erro ao obter avaliações: {e}")
            raise InternalServerError("Erro ao obter avaliações.")

    def get_by_id(self, review_id):
        """Busca uma avaliação específica pelo ID."""
        try:
            avaliacao = ReviewRepository.get_by_id(review_id)
            logger.info(f"Avaliação {review_id} encontrada.")
            return avaliacao
        except NotFoundError:
            logger.warning(f"Avaliação com ID {review_id} não encontrada.")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar avaliação {review_id}: {e}")
            raise InternalServerError("Erro ao buscar avaliação.")

    def create(self, data):
        """Cria uma nova avaliação para um projeto específico."""
        try:
            avaliacao_data = self.schema.load(data)

            projeto = ProjectRepository.get_by_id(avaliacao_data['projeto_id'])
            if not projeto:
                logger.warning("Projeto não encontrado para avaliação.")
                raise NotFoundError(resource="Projeto", message="Projeto não encontrado.")

            if projeto.avaliacao:
                logger.warning("Tentativa de avaliação para projeto já avaliado.")
                raise ConflictError(resource="Projeto", message="O projeto já possui uma avaliação.")

            avaliacao = ReviewRepository.create(avaliacao_data)
            logger.info(f"Avaliação criada com sucesso para o projeto {projeto.id}.")
            return avaliacao
        except ValidationError as err:
            logger.warning(f"Erro na validação da avaliação: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao criar avaliação: {e}")
            raise InternalServerError("Erro ao criar avaliação.")

    def update(self, review_id, data):
        """Atualiza os dados de uma avaliação existente."""
        avaliacao = self.get_by_id(review_id)

        try:
            updated_data = self.schema.load(data, partial=True)

            for key, value in updated_data.items():
                setattr(avaliacao, key, value)

            updated_avaliacao = ReviewRepository.update(avaliacao)
            logger.info(f"Avaliação {review_id} atualizada com sucesso.")
            return updated_avaliacao
        except ValidationError as err:
            logger.warning(f"Erro na validação da atualização da avaliação: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao atualizar avaliação {review_id}: {e}")
            raise InternalServerError("Erro ao atualizar avaliação.")

    def delete(self, review_id):
        """Remove uma avaliação pelo ID."""
        try:
            avaliacao = ReviewRepository.get_by_id(review_id)
            if not avaliacao:
                logger.warning("Tentativa de deletar avaliação não encontrada: ID %s", review_id)
                raise NotFoundError(resource="Avaliação", message="Avaliação não encontrada.")
            
            ReviewRepository.delete(review_id)
            logger.info("Avaliação com ID %s deletada com sucesso.", review_id)
            return {"message": "Avaliação deletada com sucesso."}
        except NotFoundError:
            raise
        except Exception as e:
            logger.error("Erro ao deletar avaliação com ID %s: %s", review_id, e)
            raise InternalServerError("Erro ao deletar avaliação.")
