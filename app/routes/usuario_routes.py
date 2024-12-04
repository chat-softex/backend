from flask import Blueprint
from app.controllers.usuario_controller import UserController
from app.middlewares.auth import jwt_required, admin_required

usuario_routes = Blueprint("usuario_routes", __name__)

# Lista todos os usuários - somente administradores
@usuario_routes.route('/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    return UserController.get_all()

# Obtém um usuário específico pelo ID - somente administradores
@usuario_routes.route('/users/<uuid:id>', methods=['GET'])
@jwt_required
@admin_required
def get_by_id_user(id):
    return UserController.get_by_id(id)

# Cria um novo usuário 
@usuario_routes.route('/users', methods=['POST'])
def create_user():
    return UserController.create()

# Atualiza um usuário específico pelo ID - somente administradores
@usuario_routes.route('/users/<uuid:id>', methods=['PUT'])
@jwt_required
@admin_required
def update_user(id):
    return UserController.update(id)

# Deleta um usuário específico pelo ID - somente administradores
@usuario_routes.route('/users/<uuid:id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_user(id):
    return UserController.delete(id)

# Rota de login de usuário (acessível a todos)
@usuario_routes.route('/users/login', methods=['POST'])
def login():
    return UserController.login()
