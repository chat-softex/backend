import tempfile
import os
import re
import logging
from io import BytesIO
from nh3 import clean_text
from validate_docbr import CPF, CNPJ
from app.services.firebase_service import FirebaseService
from app.utils.text_extractor import TextExtractor
from app.erros.custom_errors import (
    InternalServerError, ValidationError, ExternalAPIError
)

logger = logging.getLogger(__name__)


class FileUtils:
    MAX_CHARACTERS = 25000  # limite de caracteres
    SENSITIVE_PATTERNS = {
        "CNPJ": r"(?i)\b(?:CNPJ[: ]*)?(\d{2}[.\s]?\d{3}[.\s]?\d{3}[\/\s]?\d{4}[-.\s]?\d{2})\b",
        "CPF": r"(?i)\b(?:cpf[\s:.]*)?(\d{3}[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{2})\b",
        "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "Inscrição Estadual": r"\binscrição estadual[: ]?\d+\b",
        "Inscrição Municipal": r"\binscrição municipal[: ]?\d+\b",
    }

    def __init__(self):
        self.cpf_validator = CPF()
        self.cnpj_validator = CNPJ()

    @staticmethod
    def clean_text(text):
        """Remove espaços extras e caracteres especiais não necessários."""
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower()

    def _validate_cpf(self, cpf):
        """Valida CPF usando a biblioteca validate-docbr."""
        return self.cpf_validator.validate(cpf)

    def _validate_cnpj(self, cnpj):
        """Valida CNPJ usando a biblioteca validate-docbr."""
        return self.cnpj_validator.validate(cnpj)

    def _contains_sensitive_data(self, text):
        """Valida padrões sensíveis no texto extraído."""
        try:
            text = self.clean_text(text)
            sensitive_data = {}

            for label, pattern in self.SENSITIVE_PATTERNS.items():
                matches = re.findall(pattern, text, flags=re.IGNORECASE)
                if matches:
                    # validação adicional para CPFs e CNPJs
                    if label == "CPF":
                        valid_cpfs = [cpf for cpf in matches if self._validate_cpf(cpf)]
                        if valid_cpfs:
                            sensitive_data[label] = valid_cpfs
                    elif label == "CNPJ":
                        valid_cnpjs = [cnpj for cnpj in matches if self._validate_cnpj(cnpj)]
                        if valid_cnpjs:
                            sensitive_data[label] = valid_cnpjs
                    else:
                        sensitive_data[label] = matches

            return sensitive_data

        except Exception as e:
            logger.error(f"Erro inesperado ao validar dados sensíveis: {e}")
            raise InternalServerError("Erro inesperado ao validar dados sensíveis no texto.")

    def _is_within_character_limit(self, text):
        """Verifica se o texto está dentro do limite de caracteres."""
        return len(text) <= self.MAX_CHARACTERS

    def _validate_text(self, text):
        """Valida texto extraído para dados sensíveis e limite de caracteres."""
        try:
            sensitive_data = self._contains_sensitive_data(text)
            if sensitive_data:
                logger.warning(f"Documento contém dados sensíveis: {sensitive_data}")
                raise ValidationError(field="arquivo", message=f"Documento contém dados sensíveis: {sensitive_data}")
            if not self._is_within_character_limit(text):
                logger.warning("Documento excede o limite de caracteres.")
                raise ValidationError(field="arquivo", message="Documento excede o limite de caracteres permitido.")
            return True
        except ValidationError as ve:
            logger.warning(f"Erro de validação de texto: {ve.message}")
            raise 
        except Exception as e:
            logger.error(f"Erro inesperado durante validação de texto: {e}")
            raise InternalServerError("Erro inesperado ao validar o texto.")

    def is_valid_document(self, file, filename):
        """Valida documentos com base na extensão."""
        try:
            extension = filename.rsplit('.', 1)[1].lower()
            if extension not in {"pdf", "docx"}:
                raise ValidationError(field="arquivo", message="Formato de arquivo não permitido.")

            text = TextExtractor.extract_text(file.read(), extension)
            logger.info(f"Texto extraído do documento: {text}")
            self._validate_text(text)
            return True
        except ValidationError as ve:
            logger.warning(f"Erro de validação detectado: {ve.message}")
            raise
        except InternalServerError as e:
            logger.error(f"Erro interno ao validar documento: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao validar documento: {e}")
            raise InternalServerError("Erro inesperado ao validar o documento.")
        finally:
            file.seek(0)

    
    def upload_to_firebase(self, file, filename):
        """Usa o FirebaseService para fazer upload e obter a URL pública."""
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
                temp_file.write(file.read())  
                temp_file_path = temp_file.name
            
            public_url = FirebaseService.upload_file(temp_file_path, filename)
            logger.info(f"Arquivo {filename} enviado ao Firebase com URL: {public_url}")
            return public_url

        except ExternalAPIError as ve:
            logger.warning(f"Erro ao acessar o Firebase para o arquivo '{filename}': {ve.message}")
            raise

        except Exception as e:
            logger.error(f"Erro ao fazer upload para o Firebase: {e}")
            raise InternalServerError(f"Erro ao enviar o arquivo '{filename}'.") from e

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)  
                logger.info(f"Arquivo temporário {temp_file_path} removido.")



