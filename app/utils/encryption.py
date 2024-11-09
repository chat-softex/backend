# app/utils/encryption.py:
from cryptography.fernet import Fernet, InvalidToken
import os
from app.erros.custom_errors import InternalServerError, ValidationError

class Encryption:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY')
        if not self.key:
            raise InternalServerError("Chave de criptografia não encontrada.")
        self.cipher = Fernet(self.key.encode())

    def encrypt(self, data):
        try:
            return self.cipher.encrypt(data.encode())
        except Exception as e:
            raise InternalServerError("Erro ao criptografar os dados.")

    def decrypt(self, encrypted_data):
        try:
            return self.cipher.decrypt(encrypted_data).decode()
        except InvalidToken:
            raise ValidationError(field="data", message="Dados criptografados inválidos.")
        except Exception:
            raise InternalServerError("Erro ao descriptografar os dados.")
