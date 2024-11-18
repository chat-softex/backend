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
            return jsonify([empresa.to_dict() for empresa in empresas]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def get_by_id(id):
        try:
            empresa = CompanyService().get_by_id(id)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        try:
            data = request.get_json()
            empresa = CompanyService().create(data)
            return jsonify(empresa.to_dict()), 201
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
            empresa = CompanyService().update(id, data)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        try:
            CompanyService().delete(id)
            return jsonify({"message": "Empresa deletada com sucesso"}), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
