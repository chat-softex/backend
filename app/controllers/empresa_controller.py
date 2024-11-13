
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
    def obter_empresa_id(id):
        try:
            empresa = EmpresaService().get_by_id(id)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
        
    @staticmethod
    def obter_empresa_nome_fantasia(nome_fantasia):
        try:
            empresa = EmpresaService().get_by_nome_fantasia(nome_fantasia)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
        
    @staticmethod
    def obter_empresa_cnpj(cnpj):
        try:
            empresa = EmpresaService().get_by_cnpj(cnpj)
            return jsonify(empresa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
        
    @staticmethod
    def obter_empresa_email(email):
        try:
            empresa = EmpresaService().get_by_email_empresa(email)
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
    def atualizar_empresa(id):
        try:
            data = request.get_json()
            usuario = EmpresaService().update(id, data)
            return jsonify(usuario.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def deletar_empresa(id):
        try:
            EmpresaService().delete(id)
            return 'Empresa deletada com sucesso', 204  # sem corpo de resposta ****(POSSO RETORNAR UMA RESPOSTA FRANCIS? TIVEMOS ESSA DÚVIDA)****
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

