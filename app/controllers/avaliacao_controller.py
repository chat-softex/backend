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
            return jsonify([avaliacao.to_dict() for avaliacao in avaliacoes]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def get_by_id(id):
        try:
            avaliacao = ReviewService().get_by_id(id)
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        try:
            data = request.get_json()
            avaliacao = ReviewService().create(data)
            return jsonify(avaliacao.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def update(id):
        try:
            data = request.get_json()
            avaliacao = ReviewService().update(id, data)
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        try:
            ReviewService().delete(id)
            return jsonify({"message": "Avaliação deletada com sucesso"}), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
