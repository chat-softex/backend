from flask import Blueprint
from app.controllers.projeto_controller import ProjectController
from app.middlewares.auth import jwt_required, avaliador_required

projeto_routes = Blueprint("projeto_routes", __name__)

# Lista todos os projetos - apenas avaliadores
@projeto_routes.route('/projects', methods=['GET'])
@jwt_required
@avaliador_required
def get_all_projects():
    return ProjectController.get_all()

# Obtém um projeto específico pelo ID - apenas avaliadores
@projeto_routes.route('/projects/<uuid:id>', methods=['GET'])
@jwt_required
@avaliador_required
def get_by_id_project(id):
    return ProjectController.get_by_id(id)

# Cria um novo projeto - apenas avaliadores
@projeto_routes.route('/projects', methods=['POST'])
@jwt_required
@avaliador_required
def create_project():
    return ProjectController.create()

# Atualiza um projeto específico pelo ID - apenas avaliadores
@projeto_routes.route('/projects/<uuid:id>', methods=['PUT'])
@jwt_required
@avaliador_required
def update_project(id):
    return ProjectController.update(id)

# Deleta um projeto específico pelo ID - apenas avaliadores
@projeto_routes.route('/projects/<uuid:id>', methods=['DELETE'])
@jwt_required
@avaliador_required
def delete_project(id):
    return ProjectController.delete(id)


# Atualiza o status de um projeto específico - somente avaliadores
@projeto_routes.route('/projects/<uuid:id>/status', methods=['PATCH'])
@jwt_required
@avaliador_required
def update_status_project(id):
    return ProjectController.update_status(id)