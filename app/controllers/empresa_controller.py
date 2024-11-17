import logging
from flask import request, jsonify
from app.services.empresa_service import EmpresaService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class EmpresaController:
    @staticmethod
    def listar_empresas():
        try:
            empresas = EmpresaService().get_all()
            return jsonify([empresa.to_dict() for empresa in empresas]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def obter_empresa(empresa_id):
        try:
            empresa = EmpresaService().get_by_id(empresa_id)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def criar_empresa():
        try:
            data = request.get_json()
            empresa = EmpresaService().create_empresa(data)
            return jsonify(empresa.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def atualizar_empresa(empresa_id):
        try:
            data = request.get_json()
            empresa = EmpresaService().update(empresa_id, data)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def deletar_empresa(empresa_id):
        try:
            EmpresaService().delete(empresa_id)
            return jsonify({"message": "Empresa deletada com sucesso"}), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
