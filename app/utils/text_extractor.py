import PyPDF2
import pdfplumber
from io import BytesIO
from docx import Document
import logging
from app.erros.custom_errors import InternalServerError, ValidationError

logger = logging.getLogger(__name__)


class TextExtractor:
    @staticmethod
    def extract_text_pdf(file_content):
        """Extrai o texto de um arquivo PDF usando pdfplumber e PyPDF2 como fallback."""
        try:
            text = TextExtractor._extract_text_with_pdfplumber(file_content)
            if not text.strip():
                logger.warning("pdfplumber não conseguiu extrair texto. Tentando com PyPDF2.")
                text = TextExtractor._extract_text_with_pypdf2(file_content)

            if not text.strip():
                raise ValidationError(field="arquivo", message="O PDF não contém texto válido.")
            
            logger.info(f"Texto completo extraído do PDF: {text}")
            return text
        except ValidationError as ve:
            logger.warning(f"Erro de validação ao extrair texto do PDF: {ve.message}")
            raise 
        except Exception as e:
            # logger.error(f"Erro inesperado ao extrair texto do PDF: {e}", exc_info=True)
            logger.error(f"Erro inesperado ao extrair texto do PDF: {e}")
            raise InternalServerError("Erro ao processar o arquivo PDF.")

    @staticmethod
    def _extract_text_with_pdfplumber(file_content):
        """Extrai texto do PDF usando pdfplumber."""
        try:
            text = ""
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text
            return text
        except Exception as e:
            # logger.error(f"Erro ao usar pdfplumber para extrair texto: {e}", exc_info=True)
            logger.error(f"Erro ao usar pdfplumber para extrair texto: {e}")
            return ""  # retorna string vazia caso pdfplumber falhe

    @staticmethod
    def _extract_text_with_pypdf2(file_content):
        """Extrai texto do PDF usando PyPDF2 como fallback."""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
            return text
        except Exception as e:
            # logger.error(f"Erro ao usar PyPDF2 para extrair texto: {e}", exc_info=True)
            logger.error(f"Erro ao usar PyPDF2 para extrair texto: {e}")
            return ""  # retorna string vazia caso PyPDF2 falhe

    @staticmethod
    def extract_text_docx(file_content):
        """Extrai o texto de um arquivo DOCX."""
        try:
            doc = Document(BytesIO(file_content))
            text = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
            if not text.strip():
                raise ValidationError(field="arquivo", message="O documento Word não contém texto válido.")
            logger.info(f"Texto completo extraído do DOCX: {text}")
            return text
        except ValidationError as ve:
            logger.warning(f"Erro de validação ao extrair texto do DOCX: {ve.message}")
            raise 
        except Exception as e:
            # logger.error(f"Erro inesperado ao extrair texto do DOCX: {e}", exc_info=True)
            logger.error(f"Erro inesperado ao extrair texto do DOCX: {e}")
            raise InternalServerError("Erro ao processar o arquivo DOCX.")
