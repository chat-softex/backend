# app/controllers/projeto_controller.py:
import logging
from flask import request, jsonify
from app.services.projeto_service import ProjectService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError

logger = logging.getLogger(__name__)

class ProjectController:
    @staticmethod
    def get_all():
        try:
            projetos = ProjectService().get_all()
            return jsonify([projeto.to_dict() for projeto in projetos]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def get_by_id(id):
        try:
            projeto = ProjectService().get_by_id(id)
            return jsonify(projeto.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        try:
            data = request.form.to_dict()
            file = request.files.get('arquivo')
            if not file:
                raise ValidationError("arquivo", "Arquivo é obrigatório")
                
            projeto = ProjectService().create(data, file)
            return jsonify(projeto.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def update(id):
        try:
            data = request.form.to_dict()
            file = request.files.get('arquivo')
            projeto = ProjectService().update(id, data, file)
            return jsonify(projeto.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        try:
            ProjectService().delete(id)
            return '', 204  # sem corpo de resposta
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)


    @staticmethod
    def update_status(id):
        try:
            data = request.get_json()
            novo_status = data.get("status")
            projeto = ProjectService().update_status(id, novo_status)
            return jsonify(projeto.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
