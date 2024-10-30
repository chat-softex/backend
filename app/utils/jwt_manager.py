import jwt
import os
from datetime import datetime, timedelta

class JWTManager:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')

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
            raise Exception("Token expirado.")
        except jwt.InvalidTokenError:
            raise Exception("Token inválido.")
