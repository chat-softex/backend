# app/controllers/projeto_controller.py:
import logging
from flask import request, jsonify
from app.services.projeto_service import ProjectService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError, InternalServerError

logger = logging.getLogger(__name__)

class ProjectController:
    @staticmethod
    def get_all():
        try:
            projetos = ProjectService().get_all()
            logger.info("Projetos listados com sucesso.")
            return jsonify([projeto.to_dict() for projeto in projetos]), 200
        except InternalServerError as e:
            return ErrorHandler.handle_internal_server_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao listar projetos.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def get_by_id(id):
        try:
            if not id:
                raise ValidationError(field="id", message="ID inválido.")

            projeto = ProjectService().get_by_id(str(id))
            logger.info(f"Projeto {id} encontrado.")
            return jsonify(projeto.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar projeto {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        try:
            data = request.form.to_dict()
            file = request.files.get('arquivo')

            if not data:
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
            if not file:
                raise ValidationError(field="arquivo", message="Arquivo é obrigatório.")

            projeto = ProjectService().create(data, file)
            logger.info("Projeto criado com sucesso.")
            return jsonify(projeto.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao criar projeto.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def update(id):
        try:
            if not id:
                raise ValidationError(field="id", message="ID inválido.")

            data = request.form.to_dict() or {}
            file = request.files.get('arquivo')

            if not data and not file:
                raise ValidationError(field="data", message="Nenhum dado fornecido para atualização.")

            projeto = ProjectService().update(str(id), data, file)
            logger.info(f"Projeto {id} atualizado com sucesso.")
            return jsonify(projeto.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar projeto {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        try:
            if not id:
                raise ValidationError(field="id", message="ID inválido.")

            ProjectService().delete(str(id))
            logger.info(f"Projeto {id} deletado com sucesso.")
            return '', 204
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar projeto {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def update_status(id):
        try:
            if not id:
                raise ValidationError(field="id", message="ID inválido.")

            data = request.get_json()
            novo_status = data.get("status")

            if not novo_status:
                raise ValidationError(field="status", message="Status é obrigatório.")

            projeto = ProjectService().update_status(str(id), novo_status)
            logger.info(f"Status do projeto {id} atualizado para '{novo_status}'.")
            return jsonify(projeto.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar status do projeto {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
