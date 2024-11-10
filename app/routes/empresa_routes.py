# app/routes/empresa_routes.py:
from flask import Blueprint
from app.controllers.empresa_controller import EmpresaController
from app.middlewares.auth import jwt_required, admin_required

empresa_routes = Blueprint("empresa_routes", __name__)

# Lista todas as empresas - somente administradores
@empresa_routes.route('/empresas', methods=['GET'])
@jwt_required
@admin_required
def listar_empresas():
    return EmpresaController.listar_empresas()

# Obtém uma empresa específica pelo ID - somente administradores
@empresa_routes.route('/empresas/<uuid:empresa_id>', methods=['GET'])
@jwt_required
@admin_required
def obter_empresa(empresa_id):
    return EmpresaController.obter_empresa(empresa_id)

# Cria uma nova empresa - somente administradores
@empresa_routes.route('/empresas', methods=['POST'])
@jwt_required
@admin_required
def criar_empresa():
    return EmpresaController.criar_empresa()

# Atualiza uma empresa específica pelo ID - somente administradores
@empresa_routes.route('/empresas/<uuid:empresa_id>', methods=['PUT'])
@jwt_required
@admin_required
def atualizar_empresa(empresa_id):
    return EmpresaController.atualizar_empresa(empresa_id)

# Deleta uma empresa específica pelo ID - somente administradores
@empresa_routes.route('/empresas/<uuid:empresa_id>', methods=['DELETE'])
@jwt_required
@admin_required
def deletar_empresa(empresa_id):
    return EmpresaController.deletar_empresa(empresa_id)
