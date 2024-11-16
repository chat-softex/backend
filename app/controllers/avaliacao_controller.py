import logging
from flask import request, jsonify
from app.services.avaliacao_service import AvaliacaoService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class AvaliacaoController:

    # listas todas avaliações
    @staticmethod
    def listar_avaliacoes():
        try:
            avaliacoes = AvaliacaoService.get_all()
            return jsonify([avaliacao.to_dict() for avaliacao in avaliacoes]), 200
        except Exception as e:
            logger.error(f"Erro ao listar avaliações: {e}")
            return ErrorHandler.handle_error(e)

    # buscar uma avaliação
    @staticmethod
    def obter_avaliacao(avaliacao_id):
        try:
            avaliacao = AvaliacaoService.get_by_id(avaliacao_id)
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError:
            return ErrorHandler.handle_error(e)
        except Exception as e:
            logger.error(f"Erro ao obter avaliação {avaliacao_id}: {e}")
            return ErrorHandler.handle_error(e)
    # cadastrar uma avaliação
    @staticmethod
    def criar_avaliacao():
        try:
            data = request.get_json()
            if not data.get('projeto_id') or not data.get('feedback_qualitativo'):
                raise ValidationError("Faltam dados para criar a avaliação.")
            avaliacao = AvaliacaoService.create_avaliacao(data)
            return jsonify(avaliacao.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_error(e)
        except Exception as e:
            return ErrorHandler.handle_error(e)
        
    # atualizar uma avaliação
    @staticmethod
    def atualizar_avaliacao(avaliacao_id):
        try:
            data = request.get_json()
            avaliacao = AvaliacaoService.update_avaliacao(avaliacao_id, data)
            return jsonify(avaliacao.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_error(e)
        except Exception as e:
            return ErrorHandler.handle_error(e)
        
    # deletar uma avaliação     
    @staticmethod
    def deletar_avaliacao(avaliacao_id):
        try:
            AvaliacaoService.delete_avaliacao(avaliacao_id)
            return '', 204
        except NotFoundError as e:
            return ErrorHandler.handle_error(e)
        except Exception as e:
            return ErrorHandler.handle_error(e)