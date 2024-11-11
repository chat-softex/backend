import logging
from flask import request, jsonify
from app.services.empresa_service import EmpresaService
from app.erros.error_handler import ErrorHandler
from app.erros.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)


class EmpresaController:
    # listar todas empresas
    @staticmethod
    def listar_empresas():

    # buscar empresa 
    @staticmethod
    def obter_empresa(empresa_id):

    # cadastra empresa
    @staticmethod
    def criar_empresa():    

    # atualizar empresa
    @staticmethod
    def atualizar_empresa(empresa_id):

    # deletar empresa
    @staticmethod
    def deletar_empresa(empresa_id):    

