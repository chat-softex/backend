# Importa o modelo Usuario, que representa a entidade 'Usuario' no banco de dados.
from app.models.usuario_model import Usuario
# Importa a instância do banco de dados para gerenciar conexões e transações usando SQLAlchemy.
from app import db

# Classe que encapsula todas as operações CRUD (Create, Read, Update, Delete) para a entidade Usuario
class UsuarioRepository:

    # Retorna todos os usuários cadastrados no banco de dados.
    @staticmethod
    def get_all():
        return Usuario.query.all()

    # Retorna um usuário específico pelo ID.
    @staticmethod
    def get_by_id(user_id):
        return Usuario.query.get(user_id)

    # Retorna um usuário específico pelo email.
    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    # Adiciona um novo usuário ao banco de dados.
    @staticmethod
    def create(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    # Atualiza um usuário existente no banco de dados.
    @staticmethod
    def update(usuario):
        db.session.commit()
        return usuario

    # Remove um usuário do banco de dados com base no ID.
    @staticmethod
    def delete(user_id):
        usuario = Usuario.query.get(user_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
