# app/service/usuario_service.py:
import logging
from marshmallow import ValidationError
from app.repositories.usuario_repository import UsuarioRepository
from app.validators.usuario_validator import UsuarioSchema
from app.utils.encryption import Encryption
from app.utils.jwt_manager import JWTManager
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError

# Configuração do logger
logger = logging.getLogger(__name__)

class UsuarioService:
    def __init__(self):
        self.encryption = Encryption()
        self.schema = UsuarioSchema()

    def _normalize_data(self, data):
        """Converte campos específicos para letras minúsculas."""
        for key in ['nome', 'email', 'tipo']:
            if key in data and isinstance(data[key], str):
                data[key] = data[key].lower()
        return data

    def get_all(self):
        """Retorna todos os usuários cadastrados."""
        try:
            usuarios = UsuarioRepository.get_all()
            logger.info("Usuários obtidos com sucesso.")
            return usuarios
        except Exception as e:
            logger.error(f"Erro ao obter usuários: {e}")
            raise InternalServerError("Erro ao obter usuários.")

    def get_by_id(self, user_id):
        """Busca um usuário específico pelo ID."""
        try:
            usuario = UsuarioRepository.get_by_id(user_id)
            logger.info(f"Usuário {user_id} encontrado.")
            return usuario
        except NotFoundError:
            logger.warning(f"Usuário com ID {user_id} não encontrado.")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {user_id}: {e}")
            raise InternalServerError("Erro ao buscar usuário.")

    def create_usuario(self, data):
        """Cria um novo usuário, garantindo e-mail único."""
        normalized_data = self._normalize_data(data)

        if UsuarioRepository.get_by_email(normalized_data['email']):
            logger.warning("Tentativa de criação com e-mail já cadastrado.")
            raise ConflictError(resource="E-mail", message="E-mail já está cadastrado.")

        try:
            usuario_data = self.schema.load(normalized_data)
            usuario_data['senha'] = self.encryption.encrypt(usuario_data['senha'])
            usuario = UsuarioRepository.create(usuario_data)
            logger.info(f"Usuário criado com sucesso: ID {usuario.id}")
            return usuario
        except ValidationError as err:
            logger.warning(f"Erro na validação: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            raise InternalServerError("Erro ao criar usuário.")

    def update(self, user_id, data):
        """Atualiza os dados de um usuário."""
        usuario = self.get_by_id(user_id)

        normalized_data = self._normalize_data(data)

        if 'email' in normalized_data and normalized_data['email'] != usuario.email:
            if UsuarioRepository.get_by_email(normalized_data['email']):
                logger.warning(f"E-mail {normalized_data['email']} já em uso.")
                raise ConflictError(resource="E-mail", message="E-mail já está cadastrado.")

        try:
            updated_data = self.schema.load(normalized_data, partial=True)
            if 'senha' in updated_data:
                updated_data['senha'] = self.encryption.encrypt(updated_data['senha'])

            for key, value in updated_data.items():
                setattr(usuario, key, value)

            updated_usuario = UsuarioRepository.update(usuario)
            logger.info(f"Usuário {user_id} atualizado com sucesso.")
            return updated_usuario
        except ValidationError as err:
            logger.warning(f"Erro na validação dos dados: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
            raise InternalServerError("Erro ao atualizar usuário.")

    def delete(self, user_id):
        """Remove um usuário pelo ID."""
        usuario = self.get_by_id(user_id)

        try:
            UsuarioRepository.delete(user_id)
            logger.info(f"Usuário {user_id} deletado com sucesso.")
            return {"message": "Usuário deletado com sucesso."}
        except Exception as e:
            logger.error(f"Erro ao deletar usuário {user_id}: {e}")
            raise InternalServerError("Erro ao deletar usuário.")

    def login(self, email, senha):
        """Autentica um usuário e gera um token JWT."""
        usuario = self.get_by_email(email.lower())

        if not self.encryption.decrypt(usuario.senha) == senha:
            logger.warning("Tentativa de login com senha inválida.")
            raise ValidationError("Senha inválida.")

        token = JWTManager.create_token({"id": str(usuario.id), "tipo": usuario.tipo})
        logger.info(f"Usuário {usuario.id} autenticado com sucesso.")
        return {"token": token, "tipo": usuario.tipo}
