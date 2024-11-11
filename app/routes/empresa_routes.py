from flask import Blueprint
from app.controllers.empresa_controller import EmpresaController
from app.middlewares.auth import jwt_required, admin_required

empresa_routes = Blueprint("empresa_routes", __name__)

# Lista todas as empresas - somente administradores - Rota '/empresas' - metodo 'GET'
def listar_empresas():
   

# Obtém uma empresa específica pelo ID - somente administradores - Rota '/empresas/<uuid:empresa_id>' - metodo 'GET'
def obter_empresa(empresa_id):
    

# Cria uma nova empresa - somente administradores - Rota '/empresas' - metodo 'POST'
def criar_empresa():
    

# Atualiza uma empresa específica pelo ID - somente administradores - Rota '/empresas/<uuid:empresa_id>', - metodo 'PUT' 
def atualizar_empresa(empresa_id):
    

# Deleta uma empresa específica pelo ID - somente administradores - Rota '/empresas/<uuid:empresa_id>', - metodo 'DELETE' 
def deletar_empresa(empresa_id):
    

