# app/utils/file_utils.py:
import os
import re
import PyPDF2
from io import BytesIO
from app.services.firebase_service import FirebaseService
from docx import Document  # Para trabalhar com arquivos DOCX

class FileUtils:
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

    def is_valid_pdf(self, file):
        """Verifica se o PDF contém texto e remove dados sensíveis."""
        try:
            file_stream = BytesIO(file.read())
            pdf_reader = PyPDF2.PdfReader(file_stream)
            text = ""
            
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                page_text = self._remove_sensitive_data(page_text)  # Remove dados sensíveis
                text += page_text
                
            return bool(text.strip())  # Retorna True se o PDF tiver conteúdo útil
        except Exception as e:
            print(f"Erro ao processar o PDF: {e}")
            return False
        finally:
            file.seek(0)  # Retorna ao início do arquivo para que possa ser lido novamente

    def is_valid_docx(self, file):
        """Verifica se o DOCX contém texto e remove dados sensíveis."""
        try:
            file_stream = BytesIO(file.read())
            doc = Document(file_stream)
            text = ""
            
            for paragraph in doc.paragraphs:
                para_text = paragraph.text or ""
                para_text = self._remove_sensitive_data(para_text)  # Remove dados sensíveis
                text += para_text + "\n"
            
            return bool(text.strip())  # Retorna True se o DOCX tiver conteúdo útil
        except Exception as e:
            print(f"Erro ao processar o DOCX: {e}")
            return False
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
            return False

    def upload_to_firebase(self, file, filename):
        """Usa o FirebaseService para fazer upload e obter a URL pública."""
        file_path = f"/tmp/{filename}"  # Salva temporariamente o arquivo para upload
        with open(file_path, 'wb') as f:
            f.write(file.read())
        file.seek(0)  # Reseta o ponteiro do arquivo

        # Faz o upload e obtém a URL
        public_url = FirebaseService.upload_file(file_path, filename)
        
        # Remove o arquivo temporário após o upload
        os.remove(file_path)
        
        return public_url
