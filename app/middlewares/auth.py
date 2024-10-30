from flask import request, jsonify
from functools import wraps
from app.utils.jwt_manager import JWTManager
from app.repositories.usuario_repository import UsuarioRepository

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token é obrigatório'}), 401

        try:
            token_data = JWTManager.decode_token(token.split()[1])
            request.user = UsuarioRepository.get_by_id(token_data['data']['id'])  # Armazena o usuário na requisição
        except Exception as e:
            return jsonify({'message': str(e)}), 401

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.user or request.user.tipo != 'administrador':
            return jsonify({'message': 'Acesso restrito aos administradores'}), 403
        return f(*args, **kwargs)
    return decorated

def avaliador_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.user or request.user.tipo != 'avaliador':
            return jsonify({'message': 'Acesso restrito aos avaliadores'}), 403
        return f(*args, **kwargs)
    return decorated
