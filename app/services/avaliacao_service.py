from marshmallow import Schema, fields, validate, ValidationError
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.utils.encryption import Encryption
from app.utils.jwt_manager import JWTManager

# Schema de validação de Usuario
class AvaliacaoSchema(Schema):
    # A validação por Regexp foi alterada para aceitar o formato de UUID no padrão '8-4-4-4-12'
    id = fields.String(
        required=True, validate=validate.Regexp(
                r'\b[0-9a-z]{8}-[0-9a-z]{4}-[1-5][0-9a-z]{3}-[89ab][0-9a-z]{3}-[0-9a-z]{12}\b'
    ))
    # A validação por Regexp foi alterada para aceitar o formato de UUID no padrão '8-4-4-4-12'
    projeto_id = fields.String(
        required=True, validate=validate.Regexp(
                r'\b[0-9a-z]{8}-[0-9a-z]{4}-[1-5][0-9a-z]{3}-[89ab][0-9a-z]{3}-[0-9a-z]{12}\b'
    ))
    # A validação por Regexp foi alterada para aceitar o formato de data e hora no padrão 'YYYY-MM-DD HH:MM:SS'
    data_avaliacao = fields.String(
        required=True, validate=validate.Regexp(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    )
    feedback_qualitativo = fields.String(required=True, validate=validate.Length(min=10))

class AvaliacaoService:
    # Converte os campos id e projeto_id para letras minúsculas.
    def _normalize_data(self, data):
        if 'id' in data:
            data['nome'] = data['nome'].lower()
        if 'projeto_id' in data:
            data['projeto_id'] = data['projeto_id'].lower()
        return data

    # Retorna todas as avaliações cadastradas.
    def get_all(self):
        return AvaliacaoRepository.get_all()

    # Retorna uma avaliação pelo ID de avaliação ou ID do projeto.
    def get_by_id(self, id, tipo):
        avaliacao = None
        if (tipo=='avaliacao'):
            avaliacao = AvaliacaoRepository.get_by_id(id.lower())
        elif (tipo=='projeto'):
            avaliacao = AvaliacaoRepository.get_by_projeto_id(id.lower())
        else:
            raise Exception("Tipo de avaliação inválido.")

        if not avaliacao:
            raise Exception("Avaliação não encontrada.")
        return avaliacao
    
    # Cria uma nova avaliação.
    def create_avaliacao(self, data):
        try:
            # Normaliza os dados para letras minúsculas
            normalized_data = self._normalize_data(data)

            # Verifica se a avaliação já existe pelo id da avaliação
            if AvaliacaoRepository.get_by_id(normalized_data['id']):
                raise Exception("Avaliação já está cadastrada.")

            # Verifica se a avaliação já existe pelo id do projeto
            if AvaliacaoRepository.get_by_projeto_id(normalized_data['projeto_id']):
                raise Exception("Avaliação já está cadastrada.")

            avaliacao_data = AvaliacaoSchema().load(normalized_data)

            return AvaliacaoRepository.create(avaliacao_data)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Atualiza os dados de uma avaliação pelo id da avaliação ou id do projeto.
    def update_by_id(self, id, data, tipo):
        avaliacao = None
        if (tipo=='avaliacao'):
            avaliacao = AvaliacaoRepository.get_by_id(id)
        elif (tipo=='projeto'):
            avaliacao = AvaliacaoRepository.get_by_projeto_id(id)
        else:
            raise Exception("Tipo de avaliação inválido.")

        if not avaliacao:
            raise Exception("Avaliação não encontrada.")

        try:
            # Normaliza os dados para letras minúsculas
            normalized_data = self._normalize_data(data)
            updated_data = AvaliacaoRepository().load(normalized_data, partial=True)

            # Valida se passou pelo menos um campo para atualizar
            if not any(key in updated_data for key in avaliacao.__dict__.keys()):
                raise Exception("Nenhum dado foi passado para atualizar.")

            # Atualiza os atributos da avaliação
            for key, value in updated_data.items():
                setattr(avaliacao, key, value)

            return AvaliacaoRepository.update(avaliacao)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")


    # Deleta uma avaliação pelo ID.
    def delete(self, id, tipo):
        avaliacao = None
        if (tipo=='avaliacao'):
            avaliacao = AvaliacaoRepository.get_by_id(id)
        elif (tipo=='projeto'):
            avaliacao = AvaliacaoRepository.get_by_projeto_id(id)
        else:
            raise Exception("Tipo de avaliação inválido.")

        if not avaliacao:
            raise Exception("Avaliação não encontrada.")
        AvaliacaoRepository.delete(avaliacao.id)
        return {"message": "Avaliação deletada com sucesso."}
