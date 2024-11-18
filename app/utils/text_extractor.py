# app/utils/text_extractor.py:
import PyPDF2
from io import BytesIO
from docx import Document
import logging
from app.erros.custom_errors import InternalServerError

logger = logging.getLogger(__name__)

class TextExtractor:
    @staticmethod
    def extract_text_pdf(file_content):
        """Extrai o texto de um arquivo PDF."""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {e}")
            raise InternalServerError("Erro ao extrair texto do arquivo PDF.")

    @staticmethod
    def extract_text_docx(file_content):
        """Extrai o texto de um arquivo DOCX."""
        try:
            doc = Document(BytesIO(file_content))
            text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            return text
        except Exception as e:
            logger.error(f"Erro ao extrair texto do DOCX: {e}")
            raise InternalServerError("Erro ao extrair texto do arquivo DOCX.")
