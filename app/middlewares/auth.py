# app/middlewares/auth.py:
import logging
from flask import request, jsonify, g
from functools import wraps
from app.utils.jwt_manager import JWTManager
from app.repositories.usuario_repository import UserRepository
from app.erros.custom_errors import UnauthorizedError, InvalidTokenError
from app.erros.error_handler import ErrorHandler

# Configuração do logger
logger = logging.getLogger(__name__)

def jwt_required(f):
    """Middleware para verificar o token JWT e reemitir se estiver próximo de expirar."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.warning("Token ausente na requisição.")
            return ErrorHandler.handle_unauthorized_error(UnauthorizedError("Token é obrigatório"))

        try:
            # verificar se o token tem o prefixo 'Bearer'
            parts = token.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            else:
                logger.warning("Formato de token inválido.")
                raise InvalidTokenError("Formato de token inválido. Use o formato 'Bearer <token>'.")

            token_data = JWTManager.decode_token(token)
            request.user = UserRepository.get_by_id(token_data['data']['id'])
            if not request.user:
                logger.warning("Usuário não encontrado para o token fornecido.")
                raise UnauthorizedError("Usuário não encontrado.")
                
            # adiciona o novo token ao header da resposta se próximo de expirar
            if 'new_token' in token_data:
                g.new_token = token_data['new_token']
                
        except UnauthorizedError as e:
            logger.warning(f"Erro de autorização: {e}")
            return ErrorHandler.handle_unauthorized_error(e)
        except InvalidTokenError as e:
            logger.error(f"Token inválido: {e}")
            return ErrorHandler.handle_invalid_token_error(e)

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Middleware para limitar o acesso aos administradores."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.user or request.user.tipo != 'administrador':
            logger.warning("Acesso não autorizado - Usuário não é administrador.")
            return ErrorHandler.handle_unauthorized_error(UnauthorizedError("Acesso restrito aos administradores"))
        return f(*args, **kwargs)
    return decorated

def avaliador_required(f):
    """Middleware para limitar o acesso aos avaliadores."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.user or request.user.tipo != 'avaliador':
            logger.warning("Acesso não autorizado - Usuário não é avaliador.")
            return ErrorHandler.handle_unauthorized_error(UnauthorizedError("Acesso restrito aos avaliadores"))
        return f(*args, **kwargs)
    return decorated
