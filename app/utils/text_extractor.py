# app/utils/text_extractor.py:
import PyPDF2
import pdfplumber
from io import BytesIO
from docx import Document
import logging
from app.erros.custom_errors import InternalServerError, ValidationError

logger = logging.getLogger(__name__)


class TextExtractor:
    @staticmethod
    def extract_text(file_content, file_type):
        """Extrai texto de arquivos PDF ou DOCX."""
        extractors = {
            "pdf": TextExtractor._extract_text_with_pdfplumber,
            "docx": TextExtractor._extract_text_with_docx
        }
        extractor = extractors.get(file_type)

        if not extractor:
            raise ValidationError(field="file_type", message="Tipo de arquivo não suportado.")

        try:
            text = extractor(file_content)

            # Fallback para PyPDF2 no caso de PDFs
            if file_type == "pdf" and not text.strip():
                logger.warning("pdfplumber não conseguiu extrair texto. Tentando com PyPDF2.")
                text = TextExtractor._extract_text_with_pypdf2(file_content)

            if not text.strip():
                raise ValidationError(field="arquivo", message="O arquivo não contém texto válido.")

            logger.info(f"Texto extraído do arquivo: {text}")
            return text
        except ValidationError as ve:
            logger.warning(f"Erro de validação ao extrair texto: {ve.message}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair texto: {e}")
            raise InternalServerError("Erro ao processar o arquivo.")

    @staticmethod
    def _extract_text_with_pdfplumber(file_content):
        """Extrai texto de PDFs usando pdfplumber."""
        try:
            text = ""
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text
            return text
        except Exception as e:
            logger.error(f"Erro ao usar pdfplumber para extrair texto: {e}")
            return ""  # Retorna string vazia caso pdfplumber falhe

    @staticmethod
    def _extract_text_with_pypdf2(file_content):
        """Extrai texto de PDFs usando PyPDF2 como fallback."""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
            return text
        except Exception as e:
            logger.error(f"Erro ao usar PyPDF2 para extrair texto: {e}")
            return ""  # Retorna string vazia caso PyPDF2 falhe

    @staticmethod
    def _extract_text_with_docx(file_content):
        """Extrai texto de arquivos DOCX."""
        try:
            doc = Document(BytesIO(file_content))
            return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
        except Exception as e:
            logger.error(f"Erro ao usar docx para extrair texto: {e}")
            return ""  # Retorna string vazia caso falhe
