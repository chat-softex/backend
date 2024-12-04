from flask import Blueprint
from app.controllers.avaliacao_controller import ReviewController
from app.middlewares.auth import jwt_required, avaliador_required

avaliacao_routes = Blueprint("avaliacao_routes", __name__)

# Lista todas as avaliações - somente avaliadores
@avaliacao_routes.route('/reviews', methods=['GET'])
@jwt_required
@avaliador_required
def get_all_reviews():
    return ReviewController.get_all()

# Obtém uma avaliação específica pelo ID - somente avaliadores
@avaliacao_routes.route('/reviews/<uuid:id>', methods=['GET'])
@jwt_required
@avaliador_required
def get_by_id_review(id):
    return ReviewController.get_by_id(id)

# Cria uma nova avaliação - somente avaliadores
@avaliacao_routes.route('/reviews', methods=['POST'])
@jwt_required
@avaliador_required
def create_review():
    return ReviewController.create()

# Atualiza uma avaliação específica pelo ID - somente avaliadores
@avaliacao_routes.route('/reviews/<uuid:id>', methods=['PUT'])
@jwt_required
@avaliador_required
def update_review(id):
    return ReviewController.update(id)

# Deleta uma avaliação específica pelo ID - somente avaliadores
@avaliacao_routes.route('/reviews/<uuid:id>', methods=['DELETE'])
@jwt_required
@avaliador_required
def delete_review(id):
    return ReviewController.delete(id)
