from flask import Blueprint
from app.controllers.avaliacao_controller import AvaliacaoController
from app.middlewares.auth import jwt_required, avaliador_required

avaliacao_routes = Blueprint("avaliacao_routes", __name__)

# Lista todas as avaliações - somente avaliadores - Rota '/avaliacoes' - metodo 'GET'
def listar_avaliacoes():
   

# Obtém uma avaliação específica pelo ID - somente avaliadores Rota '/avaliacoes/<uuid:avaliacao_id>' - metodo 'GET'
def obter_avaliacao(avaliacao_id):
    

# Cria uma nova avaliação - somente avaliadores Rota '/avaliacoes' - metodo 'POST'
def criar_avaliacao():
    

# Atualiza uma avaliação específica pelo ID - somente avaliadores Rota '/avaliacoes/<uuid:avaliacao_id>' - metodo 'PUT'
def atualizar_avaliacao(avaliacao_id):
    

# Deleta uma avaliação específica pelo ID - somente avaliadores Rota '/avaliacoes/<uuid:avaliacao_id>' - metodo 'DELETE'
def deletar_avaliacao(avaliacao_id):
    
