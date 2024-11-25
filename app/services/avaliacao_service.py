# app/service/avaliacao_service.py
import logging
from marshmallow import ValidationError
from app.repositories.avaliacao_repository import ReviewRepository
from app.repositories.projeto_repository import ProjectRepository
from app.services.projeto_service import ProjectService
from app.validators.avaliacao_validator import ReviewSchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError
import uuid
from app.services.ia_service import IaService 

logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self):
        self.schema = ReviewSchema()
        self.ia_service = IaService()  

    def get_all(self):
        """Retorna todas as avaliações cadastradas com seus projetos e avaliadores."""
        try:
            avaliacoes = ReviewRepository.get_all()
            logger.info("Avaliações obtidas com sucesso.")
            return avaliacoes
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar avaiações: {e}")
            raise InternalServerError("Erro inesperado ao buscar avaliações.")

    def get_by_id(self, review_id):
        """Busca uma avaliação específica pelo ID."""
        try:
            if not review_id or not isinstance(review_id, str):
                raise ValidationError(field="review_id", message="ID inválido.")
            
            avaliacao = ReviewRepository.get_by_id(review_id)
            if not avaliacao:
                logger.warning(f"Avaliação com ID {review_id} não encontrada.")
                raise NotFoundError(resource="Avaliação", message="Avaliação não encontrada.")
            
            logger.info(f"Avaliação {review_id} encontrada com sucesso.")
            return avaliacao
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar avaliação {review_id}: {e}")
            raise InternalServerError("Erro inesperado ao buscar avaliação.")

    def create(self, data):
        """Cria uma nova avaliação para um projeto específico."""
        try:
            logger.info(f"Dados recebidos para criar avaliação: {data}")

            # verificar se o projeto_id é fornecido
            projeto_id = data.get("projeto_id")

        
            if not projeto_id or not isinstance(projeto_id, str):
                raise ValidationError(field="projeto_id", message="ID inválido.")
            
            projeto = ProjectRepository.get_by_id(projeto_id)
            
            if not projeto:
                logger.warning(f"Projeto não encontrado para ID: {projeto_id}")
                raise NotFoundError(resource="Projeto", message="Projeto não encontrado.")

            # verifica se o projeto já foi avaliado
            if projeto.avaliacao:
                logger.warning(f"Projeto {projeto_id} já possui uma avaliação.")
                raise ConflictError(resource="Projeto", message="O projeto já possui uma avaliação.")

            # realiza análise usando IaService
            projeto_texto = self.ia_service.obter_texto_projeto(projeto.id)
            feedback_qualitativo = self.ia_service.enviar_para_analise(projeto_texto)

            # adiciona o feedback ao dicionário de dados
            data['feedback_qualitativo'] = feedback_qualitativo

            # validação final com todos os campos presentes
            avaliacao_data = self.schema.load(data)

            # persiste no banco via repositório
            avaliacao = ReviewRepository.create(avaliacao_data)
            logger.info(f"Avaliação criada com sucesso para o projeto {projeto.id}.")
            return avaliacao

        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.messages}")
            raise
        except NotFoundError as err:
            logger.warning(f"Projeto não encontrado: {err}")
            raise
        except ConflictError as err:
            logger.warning(f"Conflito detectado: {err}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar avaliação: {e}")
            raise InternalServerError("Erro inesperado ao criar avaliação.")



    def update(self, review_id, data):
        """Atualiza os dados de uma avaliação existente."""
        try:
            if not review_id or not isinstance(review_id, str):
                raise ValidationError(field="review_id", message="ID inválido.")
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados inválidos para atualização.")

            avaliacao = self.get_by_id(review_id)

            updated_data = self.schema.load(data, partial=True)

            for key, value in updated_data.items():
                setattr(avaliacao, key, value)

            updated_avaliacao = ReviewRepository.update(avaliacao)
            logger.info(f"Avaliação com ID {review_id} atualizada com sucesso.")
            return updated_avaliacao
        
        except ValidationError as err:
             # tratamento para erros de validação
            logger.warning(f"[ValidationError] {err.messages}")
            raise ValidationError(err.messages)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar avaliação {review_id}: {e}")
            raise InternalServerError("Erro inesperado ao atualizar avaliação.")

    def delete(self, review_id):
        """Remove uma avaliação pelo ID."""
        try:
            if not review_id or not isinstance(review_id, str):
                raise ValidationError(field="review_id", message="ID inválido.")

            avaliacao = ReviewRepository.get_by_id(review_id)
            if not avaliacao:
                logger.warning(f"Tentativa de deletar avaliação com ID {review_id} não encontrada.")
                raise NotFoundError(resource="Avaliação", message="Avaliação não encontrada.")
            
            ReviewRepository.delete(review_id)
            logger.info(f"Avaliação {review_id} deletada com sucesso.")
            return {"message": "Avaliação deletada com sucesso."}
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar avaliação {review_id}: {e}")
            raise InternalServerError("Erro inesperado ao deletar avaliação.")
