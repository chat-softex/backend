# app/routes/avaliacao_routes.py:
from flask import Blueprint
from app.controllers.avaliacao_controller import AvaliacaoController
from app.middlewares.auth import jwt_required, avaliador_required

avaliacao_routes = Blueprint("avaliacao_routes", __name__)

# Lista todas as avaliações - somente avaliadores
@avaliacao_routes.route('/avaliacoes', methods=['GET'])
@jwt_required
@avaliador_required
def listar_avaliacoes():
    return AvaliacaoController.listar_avaliacoes()

# Obtém uma avaliação específica pelo ID - somente avaliadores
@avaliacao_routes.route('/avaliacoes/<uuid:avaliacao_id>', methods=['GET'])
@jwt_required
@avaliador_required
def obter_avaliacao(avaliacao_id):
    return AvaliacaoController.obter_avaliacao(avaliacao_id)

# Cria uma nova avaliação - somente avaliadores
@avaliacao_routes.route('/avaliacoes', methods=['POST'])
@jwt_required
@avaliador_required
def criar_avaliacao():
    return AvaliacaoController.criar_avaliacao()

# Atualiza uma avaliação específica pelo ID - somente avaliadores
@avaliacao_routes.route('/avaliacoes/<uuid:avaliacao_id>', methods=['PUT'])
@jwt_required
@avaliador_required
def atualizar_avaliacao(avaliacao_id):
    return AvaliacaoController.atualizar_avaliacao(avaliacao_id)

# Deleta uma avaliação específica pelo ID - somente avaliadores
@avaliacao_routes.route('/avaliacoes/<uuid:avaliacao_id>', methods=['DELETE'])
@jwt_required
@avaliador_required
def deletar_avaliacao(avaliacao_id):
    return AvaliacaoController.deletar_avaliacao(avaliacao_id)
