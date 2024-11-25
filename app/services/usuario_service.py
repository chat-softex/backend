# app/service/usuario_service.py:
import logging
import marshmallow
from app.repositories.usuario_repository import UserRepository
from app.validators.usuario_validator import UserSchema
from app.utils.encryption import Encryption
from app.utils.jwt_manager import JWTManager
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError, ValidationError
from app.erros.error_handler import ErrorHandler

# Configuração do logger
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.encryption = Encryption()
        self.schema = UserSchema()

    def _normalize_data(self, data):
        """Converte campos específicos para letras minúsculas."""
        for key in ['nome', 'email', 'tipo']:
            if key in data and isinstance(data[key], str):
                data[key] = data[key].lower()
        return data

    def get_all(self):
        """Retorna todos os usuários cadastrados."""
        try:
            usuarios = UserRepository.get_all()
            logger.info("Usuários obtidos com sucesso.")
            return usuarios
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar usuários: {e}")
            raise InternalServerError("Erro inesperado ao buscar usuários.")
        

    def get_by_id(self, user_id):
        """Busca um usuário específico pelo ID."""
        try:
            if not user_id or not isinstance(user_id, str):
                raise ValidationError(field="user_id", message="ID inválido.")

            usuario = UserRepository.get_by_id(user_id)
            if not usuario:
                logger.warning(f"Usuário com ID {user_id} não encontrado.")
                raise NotFoundError(resource="Usuário", message="Usuário não encontrado.")
            
            logger.info(f"Usuário com ID {user_id} encontrado com sucesso.")
            return usuario
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar usuário {user_id}: {e}")
            raise InternalServerError("Erro inesperado ao buscar usuário.")
        
        

    def create(self, data):
        try:
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
        
            normalized_data = self._normalize_data(data)

            # checa duplicidade de e-mail
            if UserRepository.get_by_email(normalized_data['email']):
                logger.warning("Tentativa de criação com e-mail já cadastrado.")
                raise ConflictError(resource="E-mail", message="E-mail já está cadastrado.")

            try:
                usuario_data = self.schema.load(normalized_data)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)
            
            usuario_data['senha'] = self.encryption.encrypt(usuario_data['senha'])
            usuario = UserRepository.create(usuario_data)
            logger.info(f"Usuário criado com sucesso: ID {usuario.id}")
            return usuario
        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.message}")
            raise
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar usuário: {e}")
            raise InternalServerError("Erro inesperado ao criar usuário.")


    def update(self, user_id, data):
        """Atualiza os dados de um usuário."""
        try: 
            # validações iniciais
            if not user_id or not isinstance(user_id, str):
                raise ValidationError(field="user_id", message="ID inválido.")
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados inválidos para atualização.")
                
            # busca o usuário pelo ID para verificar se existe
            usuario = UserRepository.get_by_id(user_id)
            if not usuario:
                logger.warning(f"Usuário com ID {user_id} não encontrado.")
                raise NotFoundError(resource="Usuário", message="Usuário não encontrado.")

            # normaliza os dados
            normalized_data = self._normalize_data(data)
            

            if 'email' in normalized_data and normalized_data['email'] != usuario.email:
                if UserRepository.get_by_email(normalized_data['email']):
                    logger.warning(f"E-mail {normalized_data['email']} já em uso.")
                    raise ConflictError(resource="E-mail", message="E-mail já está cadastrado.")


            try:
                updated_data = self.schema.load(normalized_data, partial=True)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)

            if 'senha' in updated_data:
                updated_data['senha'] = self.encryption.encrypt(updated_data['senha'])

            for key, value in updated_data.items():
                setattr(usuario, key, value)

            updated_usuario = UserRepository.update(usuario)
            logger.info(f"Usuário {user_id} atualizado com sucesso.")
            return updated_usuario
        
        except NotFoundError as e:
            # repropaga o erro específico para tratamento externo
            logger.warning(f"[NotFoundError] {e}")
            raise
        except ConflictError as e:
            # repropaga conflitos de dados
            logger.warning(f"[ConflictError] {e}")
            raise
        except ValidationError as err:
             # tratamento para erros de validação
            logger.warning(f"[ValidationError] {err.message}")
            raise 
        except Exception as e:
            # tratamento de erros genéricos
            logger.error(f"Erro inesperado ao atualizar usuário {user_id}: {e}")
            raise InternalServerError("Erro inesperado ao atualizar usuário.")


    def delete(self, user_id):
        """Remove um usuário pelo ID."""
        try:
            if not user_id or not isinstance(user_id, str):  # validação preliminar
                raise ValidationError(field="user_id", message="ID inválido.")

            # busca o usuário pelo ID para verificar se existe
            usuario = UserRepository.get_by_id(user_id)
            if not usuario:
                logger.warning(f"Tentativa de deletar usuário com ID {user_id} não encontrado.")
                raise NotFoundError(resource="Usuário", message="Usuário não encontrado.")
            
            # deleta o usuário
            UserRepository.delete(user_id)
            logger.info(f"Usuário {user_id} deletado com sucesso.")
            return {"message": "Usuário deletado com sucesso."}
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar usuário {user_id}: {e}")
            raise InternalServerError("Erro inesperado ao deletar usuário.")



    def login(self, email, senha):
        """Autentica um usuário e gera um token JWT."""
        try:
            if not email or not senha:
                raise ValidationError(field="credentials", message="Email e senha são obrigatórios.")

            usuario = UserRepository.get_by_email(email.lower())

            if not usuario:
                logger.warning("Tentativa de login com e-mail não registrado.")
                raise ValidationError(field="email", message="E-mail ou senha inválidos.")

            senha_descriptografada = self.encryption.decrypt(usuario.senha)
            if senha_descriptografada != senha:
                logger.warning("Tentativa de login com senha inválida.")
                raise ValidationError(field="senha", message="E-mail ou senha inválidos.")
            
            token = JWTManager.create_token({"id": str(usuario.id), "tipo": usuario.tipo})
            logger.info(f"Usuário {usuario.id} autenticado com sucesso.")
            return {"token": token, "tipo": usuario.tipo}
                
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao autenticar: {e}")
            raise InternalServerError("Erro inesperado ao autenticar.")
        

