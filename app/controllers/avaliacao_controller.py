# app/controllers/avaliacao_controller.py:
import logging
from flask import request, jsonify
from app.services.avaliacao_service import ReviewService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class ReviewController:
    @staticmethod
    def get_all():
        try:
            avaliacoes = ReviewService().get_all()
            logger.info("Avaliações listadas com sucesso.")
            return jsonify([avaliacao.to_dict() for avaliacao in avaliacoes]), 200
        except Exception as e:
            logger.error("Erro inesperado.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def get_by_id(id):
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )

            avaliacao = ReviewService().get_by_id(str(id))
            logger.info(f"Revisão {id} encontrado.")
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar avaliação {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
            avaliacao = ReviewService().create(data)
            logger.info("Avaliação criada com sucesso.")
            return jsonify(avaliacao.to_dict()), 201
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao criar avaliação.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def update(id):
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
            avaliacao = ReviewService().update(str(id), data)
            logger.info(f"Avaliação {id} atualizada com sucesso.")
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar avaliação {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )
            ReviewService().delete(str(id))
            logger.info(f"Avaliação {id} deletada com sucesso.")
            return '', 204  # sem corpo de resposta
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar avaliação {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
