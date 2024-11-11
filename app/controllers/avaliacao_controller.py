import logging
from flask import request, jsonify
from app.services.avaliacao_service import AvaliacaoService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class AvaliacaoController:

    # listas todas avaliações
    @staticmethod
    def listar_avaliacoes():
        
    # buscar uma avaliação
    @staticmethod
    def obter_avaliacao(avaliacao_id):
     
    # cadastrar uma avaliação
    @staticmethod
    def criar_avaliacao():
      
    # atualizar uma avaliação
    @staticmethod
    def atualizar_avaliacao(avaliacao_id):
        
    # deletar uma avaliação     
    @staticmethod
    def deletar_avaliacao(avaliacao_id):
        
