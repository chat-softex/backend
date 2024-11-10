# app/routes/usuario_routes.py:
from flask import Blueprint
from app.controllers.usuario_controller import UsuarioController
from app.middlewares.auth import jwt_required, admin_required

usuario_routes = Blueprint("usuario_routes", __name__)

# Lista todos os usuários - somente administradores
@usuario_routes.route('/usuarios', methods=['GET'])
@jwt_required
@admin_required
def listar_usuarios():
    return UsuarioController.listar_usuarios()

# Obtém um usuário específico pelo ID - somente administradores
@usuario_routes.route('/usuarios/<uuid:usuario_id>', methods=['GET'])
@jwt_required
@admin_required
def obter_usuario(usuario_id):
    return UsuarioController.obter_usuario(usuario_id)

# Cria um novo usuário - somente administradores
@usuario_routes.route('/usuarios', methods=['POST'])
@jwt_required
@admin_required
def criar_usuario():
    return UsuarioController.criar_usuario()

# Atualiza um usuário específico pelo ID - somente administradores
@usuario_routes.route('/usuarios/<uuid:usuario_id>', methods=['PUT'])
@jwt_required
@admin_required
def atualizar_usuario(usuario_id):
    return UsuarioController.atualizar_usuario(usuario_id)

# Deleta um usuário específico pelo ID - somente administradores
@usuario_routes.route('/usuarios/<uuid:usuario_id>', methods=['DELETE'])
@jwt_required
@admin_required
def deletar_usuario(usuario_id):
    return UsuarioController.deletar_usuario(usuario_id)

# Rota de login de usuário (acessível a todos)
@usuario_routes.route('/usuarios/login', methods=['POST'])
def login():
    return UsuarioController.login()
