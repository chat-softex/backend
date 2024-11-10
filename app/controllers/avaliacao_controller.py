# app/controllers/avaliacao_controller.py:
import logging
from flask import request, jsonify
from app.services.avaliacao_service import AvaliacaoService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class AvaliacaoController:
    @staticmethod
    def listar_avaliacoes():
        try:
            avaliacoes = AvaliacaoService().get_all()
            return jsonify([avaliacao.to_dict() for avaliacao in avaliacoes]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def obter_avaliacao(avaliacao_id):
        try:
            avaliacao = AvaliacaoService().get_by_id(avaliacao_id)
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def criar_avaliacao():
        try:
            data = request.get_json()
            avaliacao = AvaliacaoService().create_avaliacao(data)
            return jsonify(avaliacao.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def atualizar_avaliacao(avaliacao_id):
        try:
            data = request.get_json()
            avaliacao = AvaliacaoService().update(avaliacao_id, data)
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def deletar_avaliacao(avaliacao_id):
        try:
            AvaliacaoService().delete(avaliacao_id)
            return jsonify({"message": "Avaliação deletada com sucesso"}), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
