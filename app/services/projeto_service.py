# app/service/projeto_service.py:
import logging
import marshmallow
from app.repositories.projeto_repository import ProjectRepository
from app.utils.file_utils import FileUtils
from app.validators.projeto_validator import ProjectSchema
from app.erros.custom_errors import NotFoundError, ConflictError, InternalServerError, ValidationError, ExternalAPIError
from app.erros.error_handler import ErrorHandler

# Configuração do logger
logger = logging.getLogger(__name__)

class ProjectService:
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    def __init__(self):
        self.file_utils = FileUtils()
        self.schema = ProjectSchema()

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
            projetos = ProjectRepository.get_all()
            logger.info("Projetos obtidos com sucesso.")
            return projetos
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar projetos: {e}")
            raise InternalServerError("Erro inesperado ao buscar projetos.")

    def get_by_id(self, project_id):
        """Busca um projeto específico pelo ID."""
        try:
            if not project_id or not isinstance(project_id, str):
                raise ValidationError(field="project_id", message="ID inválido.")
            
            projeto = ProjectRepository.get_by_id(project_id)
            if not projeto:
                logger.warning(f"Projeto com ID {project_id} não encontrado.")
                raise NotFoundError(resource="Projeto", message="Projeto não encontrado.")       
            logger.info(f"Projeto {project_id} encontrado com sucesso.")
            return projeto
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar projeto {project_id}: {e}")
            raise InternalServerError("Erro inesperado ao buscar projeto.")

    
    def create(self, data, file):
        try:
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")

            if not file or not self._is_allowed_file(file.filename):
                raise ValidationError(field="arquivo", message="Somente arquivos PDF, DOC e DOCX são permitidos.")

            # Valida o conteúdo do arquivo com if explícito
            if not self.file_utils.is_valid_document(file, file.filename):
                logger.warning("Documento contém dados sensíveis.")
                raise ValidationError(field="arquivo", message="Documento contém dados sensíveis.")


            try:
                file_url = self.file_utils.upload_to_firebase(file, file.filename)
            except ExternalAPIError as api_error:
                logger.error(f"Erro ao utilizar Firebase: {api_error.message}")
                raise

            data['arquivo'] = file_url

            normalized_data = self._normalize_data(data)


            try:
                projeto_data = self.schema.load(normalized_data)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)

            projeto = ProjectRepository.create(projeto_data)
            logger.info(f"Projeto criado com sucesso: ID {projeto.id}")
            return projeto

        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.message}")
            raise 
        except ConflictError as e:
            logger.warning(f"Conflito ao criar projeto: {e.message}")
            raise
        except ExternalAPIError as err:
            logger.error(f"Erro na integração com Firebase: {err.message}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar projeto: {e}")
            raise InternalServerError("Erro ao criar projeto.")

    def update(self, project_id, data=None, file=None):
        try:
            if not project_id or not isinstance(project_id, str):
                raise ValidationError(field="project_id", message="ID inválido.")

            projeto = self.get_by_id(project_id)

            if file:
                if not self._is_allowed_file(file.filename):
                    raise ValidationError(field="arquivo", message="Somente arquivos PDF, DOC e DOCX são permitidos.")

                
                # Valida o conteúdo do arquivo com if explícito
                if not self.file_utils.is_valid_document(file, file.filename):
                    logger.warning("Documento contém dados sensíveis.")
                    raise ValidationError(field="arquivo", message="Documento contém dados sensíveis.")

                try:
                    file_url = self.file_utils.upload_to_firebase(file, file.filename)
                except ExternalAPIError as api_error:
                    logger.error(f"Erro ao utilizar Firebase: {api_error.message}")
                    raise

                # file_url = self.file_utils.upload_to_firebase(file, file.filename)
                data = data or {}
                data['arquivo'] = file_url

                
            # Tratamento de dados fornecidos
            if data:
                normalized_data = self._normalize_data(data)
                try:
                    projeto_data = self.schema.load(normalized_data, partial=True)
                except marshmallow.exceptions.ValidationError as marshmallow_error:
                    ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)

                # Atualização dos atributos do projeto
                for key, value in projeto_data.items():
                    setattr(projeto, key, value)    


            updated_projeto = ProjectRepository.update(projeto)
            logger.info(f"Projeto {project_id} atualizado com sucesso.")
            return updated_projeto

        except NotFoundError as e:
            logger.warning(f"Projeto não encontrado para atualização: {e}")
            raise
        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.message}")
            raise
        except ExternalAPIError as err:
            logger.error(f"Erro na integração com Firebase: {err.message}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar projeto {project_id}: {e}")
            raise InternalServerError("Erro ao atualizar projeto.")

    def update_status(self, project_id, novo_status):
        try:
            novo_status = novo_status.lower()

            if novo_status not in ['em avaliação', 'aprovado', 'reprovado']:
                raise ValidationError(field="status", message="Status inválido.")

            projeto = self.get_by_id(project_id)
            projeto.status = novo_status

            updated_projeto = ProjectRepository.update(projeto)
            logger.info(f"Status do projeto {project_id} atualizado para '{novo_status}'.")
            return updated_projeto

        except NotFoundError:
            logger.warning(f"Projeto não encontrado para atualização de status: ID {project_id}")
            raise
        except ValidationError as err:
            logger.warning(f"Erro de validação do status: {err.message}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar status do projeto {project_id}: {e}")
            raise InternalServerError("Erro ao atualizar o status do projeto.")
    


    def delete(self, project_id):
        """Remove um projeto pelo ID."""
        try:
            if not project_id or not isinstance(project_id, str):
                raise ValidationError(field="project_id", message="ID inválido.")

            projeto = ProjectRepository.get_by_id(project_id)
            if not projeto:
                logger.warning(f"Tentativa de deletar projeto com ID {project_id} não encontrado.")
                raise NotFoundError(resource="Projeto", message="Projeto não encontrado.")
            
            ProjectRepository.delete(project_id)
            logger.info(f"Projeto {project_id} deletado com sucesso.")
            return {"message": "Projeto deletado com sucesso."}
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar projeto {project_id}: {e}")
            raise InternalServerError("Erro inesperado ao deletar projeto.")
        



