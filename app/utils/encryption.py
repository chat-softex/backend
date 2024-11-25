import binascii
import os
from cryptography.fernet import Fernet, InvalidToken
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
        except Exception:
            raise InternalServerError("Erro ao criptografar os dados.")

    def decrypt(self, encrypted_data):
        try:
            # detecta e converte hexadecimal para bytes
            if isinstance(encrypted_data, str) and encrypted_data.startswith("\\x"):
                encrypted_data = binascii.unhexlify(encrypted_data[2:])  # remove o prefixo \x e converte para bytes

            return self.cipher.decrypt(encrypted_data).decode()
        except InvalidToken:
            raise ValidationError(field="data", message="Dados criptografados inválidos.")
        except Exception:
            raise InternalServerError("Erro ao descriptografar os dados.")
