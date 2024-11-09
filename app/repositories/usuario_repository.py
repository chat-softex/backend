# app/repositories/usuario_repository.py:
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.usuario_model import Usuario
from app import db
from app.erros.custom_errors import NotFoundError, InternalServerError, ConflictError

# Configuração do logger
logger = logging.getLogger("UsuarioRepository")

class UsuarioRepository:
    """Repositório para operações CRUD com a entidade Usuario"""

    # Retorna todos os usuários cadastrados no banco de dados.
    @staticmethod
    def get_all():
        try:
            usuarios = Usuario.query.all()
            logger.info("Usuários obtidos com sucesso.")
            return usuarios
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todos os usuários: {e}")
            raise InternalServerError(message="Erro ao buscar usuários.")

    # Retorna um usuário específico pelo ID.
    @staticmethod
    def get_by_id(id):
        try:
            usuario = Usuario.query.get(id)
            if not usuario:
                logger.warning(f"Usuário com ID {id} não encontrado.")
                raise NotFoundError(resource="Usuario", message="Usuário não encontrado.")
            logger.info(f"Usuário com ID {id} encontrado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar usuário com ID {id}: {e}")
            raise InternalServerError(message="Erro ao buscar usuário pelo ID.")

    # Retorna um usuário específico pelo email.
    @staticmethod
    def get_by_email(email):
        try:
            usuario = Usuario.query.filter_by(email=email).first()
            if not usuario:
                logger.warning(f"Usuário com email {email} não encontrado.")
                raise NotFoundError(resource="Usuario", message="Usuário com esse email não encontrado.")
            logger.info(f"Usuário com email {email} encontrado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar usuário com email {email}: {e}")
            raise InternalServerError(message="Erro ao buscar usuário pelo email.")

    # Adiciona um novo usuário ao banco de dados.
    @staticmethod
    def create(usuario):
        try:
            db.session.add(usuario)
            db.session.commit()
            logger.info(f"Usuário criado com sucesso: {usuario.id}")
            return usuario
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Erro de integridade ao criar usuário: {e}")
            raise ConflictError(resource="Usuario", message="Email já cadastrado.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao criar usuário: {e}")
            raise InternalServerError(message="Erro ao criar usuário.")

    # Atualiza um usuário existente no banco de dados.
    @staticmethod
    def update(usuario):
        try:
            db.session.commit()
            logger.info(f"Usuário com ID {usuario.id} atualizado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar usuário com ID {usuario.id}: {e}")
            raise InternalServerError(message="Erro ao atualizar usuário.")

    # Remove um usuário do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        try:
            usuario = UsuarioRepository.get_by_id(id)
            db.session.delete(usuario)
            db.session.commit()
            logger.info(f"Usuário com ID {id} deletado com sucesso.")
        except NotFoundError as e:
            logger.warning(f"Tentativa de deletar usuário não encontrado: ID {id}")
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar usuário com ID {id}: {e}")
            raise InternalServerError(message="Erro ao deletar usuário.")
