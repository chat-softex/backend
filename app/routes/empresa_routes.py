# app/routes/empresa_routes.py:
from flask import Blueprint
from app.controllers.empresa_controller import CompanyController
from app.middlewares.auth import jwt_required, avaliador_required

empresa_routes = Blueprint("empresa_routes", __name__)

# Lista todas as empresas - somente avaliadores
@empresa_routes.route('/companies', methods=['GET'])
@jwt_required
@avaliador_required
def get_all_companies():
    return CompanyController.get_all()

# Obtém uma empresa específica pelo ID - somente avaliadores
@empresa_routes.route('/companies/<uuid:id>', methods=['GET'])
@jwt_required
@avaliador_required
def get_by_id_company(id):
    return CompanyController.get_by_id(id)

# Cria uma nova empresa - somente avaliadores
@empresa_routes.route('/companies', methods=['POST'])
@jwt_required
@avaliador_required
def create_company():
    return CompanyController.create()

# Atualiza uma empresa específica pelo ID - somente avaliadores
@empresa_routes.route('/companies/<uuid:id>', methods=['PUT'])
@jwt_required
@avaliador_required
def update_company(id):
    return CompanyController.update(id)

# Deleta uma empresa específica pelo ID - somente avaliadores
@empresa_routes.route('/companies/<uuid:id>', methods=['DELETE'])
@jwt_required
@avaliador_required
def delete_company(id):
    return CompanyController.delete(id)
