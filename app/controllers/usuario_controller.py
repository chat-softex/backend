#app/controllers/usuario_controller.py:
import logging
from flask import request, jsonify
from app.services.usuario_service import UsuarioService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class UsuarioController:
    @staticmethod
    def listar_usuarios():
        try:
            usuarios = UsuarioService().get_all()
            return jsonify([usuario.to_dict() for usuario in usuarios]), 200
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def obter_usuario(usuario_id):
        try:
            usuario = UsuarioService().get_by_id(usuario_id)
            return jsonify(usuario.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def criar_usuario():
        try:
            data = request.get_json()
            usuario = UsuarioService().create_usuario(data)
            return jsonify(usuario.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def atualizar_usuario(usuario_id):
        try:
            data = request.get_json()
            usuario = UsuarioService().update(usuario_id, data)
            return jsonify(usuario.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def deletar_usuario(usuario_id):
        try:
            UsuarioService().delete(usuario_id)
            return '', 204  # sem corpo de resposta
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get("email")
            senha = data.get("senha")
            if not email or not senha:
                raise ValidationError("Login", "Email e senha são obrigatórios")
            
            result = UsuarioService().login(email, senha)
            return jsonify(result), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_exception(e)
