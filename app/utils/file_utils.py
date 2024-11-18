# app/utils/file_utils.py
import os
import re
import logging
from io import BytesIO
from app.services.firebase_service import FirebaseService
from app.utils.text_extractor import TextExtractor  # Importação de TextExtractor
from app.erros.custom_errors import InternalServerError, ValidationError  # Adicionando ValidationError

logger = logging.getLogger(__name__)

class FileUtils:
    MAX_CHARACTERS = 25000  # Limite de caracteres
    SENSITIVE_PATTERNS = {
        "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
        "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        "Inscrição Estadual": r"\binscrição estadual\b|\bie\b",
        "Inscrição Municipal": r"\binscrição municipal\b|\bim\b",
        "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "CEP": r"\b\d{5}-\d{3}\b",
        "Logradouro": r"\b(rua|avenida|logradouro|estrada|praça)\b\s+\w+",
        "Número": r"\bnúmero\s*\d+|\bn°\s*\d+",
        "Bairro": r"\bbairro\s+\w+",
        "Cidade": r"\bcidade\s+\w+",
        "UF": r"\b(?:AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b",
    }

    def _remove_sensitive_data(self, text):
        """Remove dados sensíveis do texto usando os padrões definidos."""
        for label, pattern in self.SENSITIVE_PATTERNS.items():
            text = re.sub(pattern, "[DADO REMOVIDO]", text, flags=re.IGNORECASE)
        return text

    def _is_within_character_limit(self, text):
        """Verifica se o texto está dentro do limite de caracteres."""
        return len(text) <= self.MAX_CHARACTERS

    def is_valid_pdf(self, file):
        """Verifica se o PDF contém texto útil dentro do limite de caracteres e remove dados sensíveis."""
        try:
            text = TextExtractor.extract_text_pdf(file.read())
            text = self._remove_sensitive_data(text)
            if not self._is_within_character_limit(text):
                raise ValidationError("file", "Documento excede o limite de caracteres permitido.")
            return bool(text.strip())
        except Exception as e:
            logger.error(f"Erro ao validar PDF: {e}")
            raise InternalServerError("Erro ao processar o arquivo PDF.")
        finally:
            file.seek(0)

    def is_valid_docx(self, file):
        """Verifica se o DOCX contém texto útil dentro do limite de caracteres e remove dados sensíveis."""
        try:
            text = TextExtractor.extract_text_docx(file.read())
            text = self._remove_sensitive_data(text)
            if not self._is_within_character_limit(text):
                raise ValidationError("file", "Documento excede o limite de caracteres permitido.")
            return bool(text.strip())
        except Exception as e:
            logger.error(f"Erro ao validar DOCX: {e}")
            raise InternalServerError("Erro ao processar o arquivo DOCX.")
        finally:
            file.seek(0)

    def is_valid_document(self, file, filename):
        """Determina a validação com base na extensão do arquivo."""
        extension = filename.rsplit('.', 1)[1].lower()
        if extension == 'pdf':
            return self.is_valid_pdf(file)
        elif extension in {'doc', 'docx'}:
            return self.is_valid_docx(file)
        else:
            raise ValidationError("file", "Formato de arquivo não permitido.")

    def upload_to_firebase(self, file, filename):
        """Usa o FirebaseService para fazer upload e obter a URL pública."""
        try:
            file_path = f"/tmp/{filename}"
            with open(file_path, 'wb') as f:
                f.write(file.read())
            file.seek(0)

            public_url = FirebaseService.upload_file(file_path, filename)
            os.remove(file_path)
            return public_url
        except Exception as e:
            logger.error(f"Erro ao fazer upload para o Firebase: {e}")
            raise InternalServerError("Erro ao fazer upload do arquivo.")
