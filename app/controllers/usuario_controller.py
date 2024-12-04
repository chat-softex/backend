import logging
from flask import request, jsonify
from app.services.usuario_service import UserService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    def get_all():
        try:
            usuarios = UserService().get_all()
            logger.info("Usuários listados com sucesso.")
            return jsonify([usuario.to_dict() for usuario in usuarios]), 200
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

            usuario = UserService().get_by_id(str(id))  # converte para string
            logger.info(f"Usuário {id} encontrado.")
            return jsonify(usuario.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar usuário {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
                

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
            usuario = UserService().create(data)
            logger.info("Usuário criado com sucesso.")
            return jsonify(usuario.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao criar usuário.", exc_info=True)
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
           
            usuario = UserService().update(str(id), data)  # converte para string
            logger.info(f"Usuário {id} atualizado com sucesso.")
            return jsonify(usuario.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar usuário {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)


    @staticmethod
    def delete(id):
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )
            
            UserService().delete(str(id))  
            logger.info(f"Usuário {id} deletado com sucesso.")
            return '', 204  
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar usuário {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)


    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get("email")
            senha = data.get("senha")
            if not email or not senha:
                raise ValidationError(field="credentials", message="Email e senha são obrigatórios.")
            
            result = UserService().login(email, senha)
            logger.info(f"Usuário autenticado com sucesso.")
            return jsonify(result), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao autenticar usuário.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
