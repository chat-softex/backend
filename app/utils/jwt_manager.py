# app/utils/jwt_manager.py:
import jwt
import os
import logging
from datetime import datetime, timedelta
from app.erros.custom_errors import UnauthorizedError, InvalidTokenError

logger = logging.getLogger(__name__)

class JWTManager:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key')
    ACCESS_EXPIRATION = int(os.getenv('ACCESS_EXPIRATION', 60))  # Minutos, padrão 60
    RENEWAL_THRESHOLD = int(os.getenv('RENEWAL_THRESHOLD', 5))   # Minutos antes do vencimento para renovação

    @staticmethod
    def create_token(data, expires_in=None):
        expiration = datetime.utcnow() + timedelta(minutes=expires_in or JWTManager.ACCESS_EXPIRATION)
        token = jwt.encode({'data': data, 'exp': expiration}, JWTManager.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, JWTManager.SECRET_KEY, algorithms=['HS256'])
            expiration = datetime.fromtimestamp(payload['exp'])
            # Reemissão de token se a expiração estiver próxima
            if (expiration - datetime.utcnow()).total_seconds() < JWTManager.RENEWAL_THRESHOLD * 60:
                new_token = JWTManager.create_token(payload['data'])
                payload['new_token'] = new_token
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado.")
            raise UnauthorizedError(message="Token expirado.")
        except jwt.InvalidTokenError:
            logger.error("Token inválido ou malformado.")
            raise InvalidTokenError(message="Token inválido ou malformado.")
        except Exception as e:
            logger.error(f"Erro inesperado na decodificação do token: {e}")
            raise InvalidTokenError("Erro na decodificação do token.")
