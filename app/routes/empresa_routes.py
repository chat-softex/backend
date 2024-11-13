
from flask import Blueprint
from app.controllers.empresa_controller import EmpresaController
from app.middlewares.auth import jwt_required, avaliador_required

empresa_routes = Blueprint("empresa_routes", __name__)

# Lista todas as empresas - somente administradores
@empresa_routes.route('/empresas', methods=['GET'])
@jwt_required
@avaliador_required
def listar_empresas():
    return EmpresaController.listar_empresas()

# Obtém uma empresa específica pelo ID - somente administradores
@empresa_routes.route('/empresas/<uuid:id>', methods=['GET'])
@jwt_required
@avaliador_required
def obter_usuario(id):
    return EmpresaController.obter_empresa_id(id)

@empresa_routes.route('/empresas/nome_fantasia', methods=['GET'])
@jwt_required
@avaliador_required
def obter_usuario(nome_fantasia):
    return EmpresaController.obter_empresa_nome_fantasia(nome_fantasia)

@empresa_routes.route('/empresas/cnpj', methods=['GET'])
@jwt_required
@avaliador_required
def obter_usuario(cnpj):
    return EmpresaController.obter_empresa_cnpj(cnpj)

@empresa_routes.route('/empresas/email', methods=['GET'])
@jwt_required
@avaliador_required
def obter_usuario(email):
    return EmpresaController.obter_empresa_email(email)

# Cria uma nova empresa - somente administradores
@empresa_routes.route('/empresas', methods=['POST'])
@jwt_required
@avaliador_required
def criar_usuario():
    return EmpresaController.criar_empresa()

# Atualiza uma empresa específica pelo ID - somente administradores
@empresa_routes.route('/empresas/<uuid:id>', methods=['PUT'])
@jwt_required
@avaliador_required
def atualizar_empresa(id):
    return EmpresaController.atualizar_empresa(id)

# Deleta uma empresa específica pelo ID - somente administradores
@empresa_routes.route('/empresas/<uuid:id>', methods=['DELETE'])
@jwt_required
@avaliador_required
def deletar_empresa(id):
    return EmpresaController.deletar_empresa(id)


