from marshmallow import Schema, fields, validate, ValidationError
from app.repositories.projeto_repository import ProjetoRepository
from app.utils.file_utils import FileUtils

# Schema de validação para Projeto
class ProjetoSchema(Schema):
    titulo_projeto = fields.String(required=True, validate=validate.Length(min=5))
    status = fields.String(
        required=True,
        validate=validate.OneOf(['em avaliação', 'aprovado', 'reprovado'])
    )
    arquivo = fields.String(required=True)
    avaliador_id = fields.UUID(required=True)
    empresa_id = fields.UUID(required=True)

class ProjetoService:
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    def __init__(self):
        self.file_utils = FileUtils()

    # Valida se o arquivo tem uma extensão permitida (PDF ou Word).
    def _is_allowed_file(self, filename):
        if '.' not in filename:
            return False
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in self.ALLOWED_EXTENSIONS

    # Converte os campos de string para letras minúsculas.
    def _normalize_data(self, data):
        if 'titulo_projeto' in data:
            data['titulo_projeto'] = data['titulo_projeto'].lower()
        if 'status' in data:
            data['status'] = data['status'].lower()
        return data

    # Retorna todos os projetos cadastrados.
    def get_all(self):
        return ProjetoRepository.get_all()

    # Busca um projeto específico pelo ID.
    def get_by_id(self, projeto_id):
        projeto = ProjetoRepository.get_by_id(projeto_id)
        if not projeto:
            raise Exception("Projeto não encontrado.")
        return projeto

    # Cria um novo projeto e faz o upload do arquivo para o Firebase.
    def create_projeto(self, data, file):
        if not self._is_allowed_file(file.filename):
            raise Exception("Somente arquivos PDF ou Word são permitidos.")

        try:
            # Normaliza os dados
            projeto_data = self._normalize_data(data)

            # Valida os dados do projeto
            projeto_data = ProjetoSchema().load(projeto_data)

            # Faz upload do arquivo para o Firebase
            file_url = self.file_utils.upload_file(file, file.filename)
            projeto_data['arquivo'] = file_url

            # Cria o projeto no banco de dados
            return ProjetoRepository.create(projeto_data)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Atualiza os dados de um projeto, com upload opcional de novo arquivo.
    def update(self, projeto_id, data, file=None):
        projeto = ProjetoRepository.get_by_id(projeto_id)
        if not projeto:
            raise Exception("Projeto não encontrado.")

        if file and not self._is_allowed_file(file.filename):
            raise Exception("Somente arquivos PDF ou Word são permitidos.")

        try:
            # Normaliza os dados
            updated_data = self._normalize_data(data)

            # Valida e carrega os dados parciais
            updated_data = ProjetoSchema().load(updated_data, partial=True)

            # Se um novo arquivo foi enviado, faz upload e atualiza a URL
            if file:
                file_url = self.file_utils.upload_file(file, file.filename)
                updated_data['arquivo'] = file_url

            # Atualiza os atributos do projeto
            for key, value in updated_data.items():
                setattr(projeto, key, value)

            return ProjetoRepository.update(projeto)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Remove um projeto pelo ID.
    def delete(self, projeto_id):
        projeto = ProjetoRepository.get_by_id(projeto_id)
        if not projeto:
            raise Exception("Projeto não encontrado.")
        ProjetoRepository.delete(projeto_id)
        return {"message": "Projeto deletado com sucesso."}

    # Atualiza o status de um projeto ('em avaliação', 'aprovado', 'reprovado').
    def update_status(self, projeto_id, status):
        projeto = ProjetoRepository.get_by_id(projeto_id)
        if not projeto:
            raise Exception("Projeto não encontrado.")

        normalized_status = status.lower()
        if normalized_status not in ['em avaliação', 'aprovado', 'reprovado']:
            raise Exception("Status inválido.")

        projeto.status = normalized_status
        return ProjetoRepository.update(projeto)
