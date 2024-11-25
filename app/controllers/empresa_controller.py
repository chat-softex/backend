# app/controllers/empresa_controller.py:
import logging
from flask import request, jsonify
from app.services.empresa_service import CompanyService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class CompanyController:
    @staticmethod
    def get_all():
        try:
            empresas = CompanyService().get_all()
            logger.info("Empresas listadas com sucesso.")
            return jsonify([empresa.to_dict() for empresa in empresas]), 200
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
            
            empresa = CompanyService().get_by_id(str(id))
            logger.info(f"Empresa {id} encontrado.")
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar empresa {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
            empresa = CompanyService().create(data)
            logger.info("Empresa criada com sucesso.")
            return jsonify(empresa.to_dict()), 201
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao criar empresa.", exc_info=True)
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
            empresa = CompanyService().update(str(id), data)
            logger.info(f"Empresa {id} atualizado com sucesso.")
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar empresa {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )

            CompanyService().delete(str(id))
            logger.info(f"Empresa {id} deletado com sucesso.")
            return '', 204 
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar empresa {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
