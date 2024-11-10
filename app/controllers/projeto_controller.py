#app/controllers/projeto_controller.py:
import logging
from flask import request, jsonify
from app.services.projeto_service import ProjetoService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError

logger = logging.getLogger(__name__)

class ProjetoController:
    @staticmethod
    def listar_projetos():
        try:
            projetos = ProjetoService().get_all()
            return jsonify([projeto.to_dict() for projeto in projetos]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def obter_projeto(projeto_id):
        try:
            projeto = ProjetoService().get_by_id(projeto_id)
            return jsonify(projeto.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def criar_projeto():
        try:
            data = request.form.to_dict()
            file = request.files.get('arquivo')
            if not file:
                raise ValidationError("arquivo", "Arquivo é obrigatório")
                
            projeto = ProjetoService().create_projeto(data, file)
            return jsonify(projeto.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def atualizar_projeto(projeto_id):
        try:
            data = request.form.to_dict()
            file = request.files.get('arquivo')
            projeto = ProjetoService().update(projeto_id, data, file)
            return jsonify(projeto.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def deletar_projeto(projeto_id):
        try:
            ProjetoService().delete(projeto_id)
            return '', 204  # sem corpo de resposta
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)


    @staticmethod
    def atualizar_status(projeto_id):
        try:
            data = request.get_json()
            novo_status = data.get("status")
            projeto = ProjetoService().update_status(projeto_id, novo_status)
            return jsonify(projeto.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)