# app/utils/jwt_manager.py:
import jwt
import os
import logging
from datetime import datetime, timedelta
from app.erros.custom_errors import UnauthorizedError, InvalidTokenError

logger = logging.getLogger(__name__)

class JWTManager:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key')

    @staticmethod
    def create_token(data, expires_in=60):
        expiration = datetime.utcnow() + timedelta(minutes=expires_in)
        token = jwt.encode({'data': data, 'exp': expiration}, JWTManager.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, JWTManager.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado.")
            raise UnauthorizedError(message="Token expirado.")
        except jwt.InvalidTokenError:
            logger.error("Token inválido ou malformado.")
            raise InvalidTokenError(message="Token inválido ou malformado.")
        except Exception as e:
            logger.error(f"Erro inesperado na decodificação do token: {e}")
            raise InvalidTokenError("Erro na decodificação do token.")
