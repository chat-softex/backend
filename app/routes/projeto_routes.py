# app/routes/projeto_routes.py:
from flask import Blueprint
from app.controllers.projeto_controller import ProjetoController
from app.middlewares.auth import jwt_required, avaliador_required

projeto_routes = Blueprint("projeto_routes", __name__)

# Lista todos os projetos - apenas avaliadores
@projeto_routes.route('/projetos', methods=['GET'])
@jwt_required
@avaliador_required
def listar_projetos():
    return ProjetoController.listar_projetos()

# Obtém um projeto específico pelo ID - apenas avaliadores
@projeto_routes.route('/projetos/<uuid:projeto_id>', methods=['GET'])
@jwt_required
@avaliador_required
def obter_projeto(projeto_id):
    return ProjetoController.obter_projeto(projeto_id)

# Cria um novo projeto - apenas avaliadores
@projeto_routes.route('/projetos', methods=['POST'])
@jwt_required
@avaliador_required
def criar_projeto():
    return ProjetoController.criar_projeto()

# Atualiza um projeto específico pelo ID - apenas avaliadores
@projeto_routes.route('/projetos/<uuid:projeto_id>', methods=['PUT'])
@jwt_required
@avaliador_required
def atualizar_projeto(projeto_id):
    return ProjetoController.atualizar_projeto(projeto_id)

# Deleta um projeto específico pelo ID - apenas avaliadores
@projeto_routes.route('/projetos/<uuid:projeto_id>', methods=['DELETE'])
@jwt_required
@avaliador_required
def deletar_projeto(projeto_id):
    return ProjetoController.deletar_projeto(projeto_id)


# Atualiza o status de um projeto específico - somente avaliadores
@projeto_routes.route('/projetos/<uuid:projeto_id>/status', methods=['PATCH'])
@jwt_required
@avaliador_required
def atualizar_status(projeto_id):
    return ProjetoController.atualizar_status(projeto_id)