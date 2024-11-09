# app/service/avaliacao_service.py
import logging
from marshmallow import ValidationError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.projeto_repository import ProjetoRepository
from app.validators.avaliacao_validator import AvaliacaoSchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError

logger = logging.getLogger(__name__)

class AvaliacaoService:
    def __init__(self):
        self.schema = AvaliacaoSchema()

    def get_all(self):
        """Retorna todas as avaliações cadastradas com seus projetos e avaliadores."""
        try:
            avaliacoes = AvaliacaoRepository.get_all()
            logger.info("Avaliações obtidas com sucesso.")
            return avaliacoes
        except Exception as e:
            logger.error(f"Erro ao obter avaliações: {e}")
            raise InternalServerError("Erro ao obter avaliações.")

    def get_by_id(self, avaliacao_id):
        """Busca uma avaliação específica pelo ID."""
        try:
            avaliacao = AvaliacaoRepository.get_by_id(avaliacao_id)
            logger.info(f"Avaliação {avaliacao_id} encontrada.")
            return avaliacao
        except NotFoundError:
            logger.warning(f"Avaliação com ID {avaliacao_id} não encontrada.")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar avaliação {avaliacao_id}: {e}")
            raise InternalServerError("Erro ao buscar avaliação.")

    def create_avaliacao(self, data):
        """Cria uma nova avaliação para um projeto específico."""
        try:
            avaliacao_data = self.schema.load(data)

            projeto = ProjetoRepository.get_by_id(avaliacao_data['projeto_id'])
            if not projeto:
                logger.warning("Projeto não encontrado para avaliação.")
                raise NotFoundError(resource="Projeto", message="Projeto não encontrado.")

            if projeto.avaliacao:
                logger.warning("Tentativa de avaliação para projeto já avaliado.")
                raise ConflictError(resource="Projeto", message="O projeto já possui uma avaliação.")

            avaliacao = AvaliacaoRepository.create(avaliacao_data)
            logger.info(f"Avaliação criada com sucesso para o projeto {projeto.id}.")
            return avaliacao
        except ValidationError as err:
            logger.warning(f"Erro na validação da avaliação: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao criar avaliação: {e}")
            raise InternalServerError("Erro ao criar avaliação.")

    def update(self, avaliacao_id, data):
        """Atualiza os dados de uma avaliação existente."""
        avaliacao = self.get_by_id(avaliacao_id)

        try:
            updated_data = self.schema.load(data, partial=True)

            for key, value in updated_data.items():
                setattr(avaliacao, key, value)

            updated_avaliacao = AvaliacaoRepository.update(avaliacao)
            logger.info(f"Avaliação {avaliacao_id} atualizada com sucesso.")
            return updated_avaliacao
        except ValidationError as err:
            logger.warning(f"Erro na validação da atualização da avaliação: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao atualizar avaliação {avaliacao_id}: {e}")
            raise InternalServerError("Erro ao atualizar avaliação.")

    def delete(self, avaliacao_id):
        """Remove uma avaliação pelo ID."""
        avaliacao = self.get_by_id(avaliacao_id)

        try:
            AvaliacaoRepository.delete(avaliacao_id)
            logger.info(f"Avaliação {avaliacao_id} deletada com sucesso.")
            return {"message": "Avaliação deletada com sucesso."}
        except Exception as e:
            logger.error(f"Erro ao deletar avaliação {avaliacao_id}: {e}")
            raise InternalServerError("Erro ao deletar avaliação.")
