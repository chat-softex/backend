# app/service/projeto_service.py:
import logging
from marshmallow import ValidationError
from app.repositories.projeto_repository import ProjetoRepository
from app.utils.file_utils import FileUtils
from app.validators.projeto_validator import ProjetoSchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError

# Configuração do logger
logger = logging.getLogger(__name__)

class ProjetoService:
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    def __init__(self):
        self.file_utils = FileUtils()
        self.schema = ProjetoSchema()

    def _is_allowed_file(self, filename):
        """Verifica se o arquivo tem uma extensão permitida (PDF, DOC, DOCX)."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def _normalize_data(self, data):
        """Converte campos específicos para letras minúsculas."""
        if 'titulo_projeto' in data:
            data['titulo_projeto'] = data['titulo_projeto'].lower()
        if 'status' in data:
            data['status'] = data['status'].lower()
        return data

    def get_all(self):
        """Retorna todos os projetos cadastrados."""
        try:
            projetos = ProjetoRepository.get_all()
            logger.info("Projetos obtidos com sucesso.")
            return projetos
        except Exception as e:
            logger.error(f"Erro ao buscar projetos: {e}")
            raise InternalServerError("Erro ao obter projetos.")

    def get_by_id(self, projeto_id):
        """Busca um projeto específico pelo ID."""
        try:
            projeto = ProjetoRepository.get_by_id(projeto_id)
            logger.info(f"Projeto {projeto_id} encontrado com sucesso.")
            return projeto
        except NotFoundError:
            logger.warning(f"Projeto com ID {projeto_id} não encontrado.")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar projeto {projeto_id}: {e}")
            raise InternalServerError("Erro ao buscar projeto.")

    def create_projeto(self, data, file):
        """Cria um novo projeto e valida o arquivo (PDF, DOC, DOCX) para o Firebase."""
        if not self._is_allowed_file(file.filename):
            logger.warning("Arquivo com extensão não permitida.")
            raise ValidationError("Somente arquivos PDF, DOC e DOCX são permitidos.")

        # Verifica se o documento é válido e não possui dados sensíveis
        if not self.file_utils.is_valid_document(file, file.filename):
            logger.warning("Documento inválido ou contém dados sensíveis.")
            raise ValidationError("O documento deve conter texto válido e não deve ter dados sensíveis.")

        try:
            projeto_data = self._normalize_data(data)
            projeto_data = self.schema.load(projeto_data)

            # Faz o upload do documento para o Firebase e obtém a URL pública
            file_url = self.file_utils.upload_to_firebase(file, file.filename)
            projeto_data['arquivo'] = file_url

            projeto = ProjetoRepository.create(projeto_data)
            logger.info(f"Projeto criado com sucesso: ID {projeto.id}")
            return projeto
        except ValidationError as err:
            logger.warning(f"Erro na validação dos dados do projeto: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao criar projeto: {e}")
            raise InternalServerError("Erro ao criar projeto.")

    def update(self, projeto_id, data, file=None):
        """Atualiza os dados de um projeto, com upload opcional de novo arquivo."""
        projeto = self.get_by_id(projeto_id)

        if file and not self._is_allowed_file(file.filename):
            logger.warning("Arquivo com extensão não permitida para atualização.")
            raise ValidationError("Somente arquivos PDF, DOC e DOCX são permitidos.")

        try:
            updated_data = self._normalize_data(data)
            updated_data = self.schema.load(updated_data, partial=True)

            if file:
                file_url = self.file_utils.upload_to_firebase(file, file.filename)
                updated_data['arquivo'] = file_url

            for key, value in updated_data.items():
                setattr(projeto, key, value)

            updated_projeto = ProjetoRepository.update(projeto)
            logger.info(f"Projeto {projeto_id} atualizado com sucesso.")
            return updated_projeto
        except ValidationError as err:
            logger.warning(f"Erro na validação dos dados do projeto: {err.messages}")
            raise ValidationError(f"Erro na validação: {err.messages}")
        except Exception as e:
            logger.error(f"Erro ao atualizar projeto {projeto_id}: {e}")
            raise InternalServerError("Erro ao atualizar projeto.")
        

    def update_status(self, projeto_id, novo_status):
        """Atualiza o status de um projeto."""
        if novo_status not in ['em avaliação', 'aprovado', 'reprovado']:
            logger.warning(f"Status inválido: {novo_status}")
            raise ValidationError(field="status", message="Status deve ser 'em avaliação', 'aprovado' ou 'reprovado'.")

        projeto = self.get_by_id(projeto_id)
        try:
            projeto.status = novo_status
            updated_projeto = ProjetoRepository.update(projeto)
            logger.info(f"Status do projeto {projeto_id} atualizado para '{novo_status}'.")
            return updated_projeto
        except Exception as e:
            logger.error(f"Erro ao atualizar status do projeto {projeto_id}: {e}")
            raise InternalServerError("Erro ao atualizar o status do projeto.")    
