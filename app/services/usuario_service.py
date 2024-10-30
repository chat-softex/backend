from marshmallow import Schema, fields, validate, ValidationError
from app.repositories.usuario_repository import UsuarioRepository
from app.utils.encryption import Encryption
from app.utils.jwt_manager import JWTManager

# Schema de validação de Usuario
class UsuarioSchema(Schema):
    nome = fields.String(
        required=True, validate=validate.Length(min=3, max=255)
    )
    email = fields.Email(required=True, validate=validate.Length(max=255))
    senha = fields.String(
        required=True,
        validate=[
            validate.Length(min=6, max=10),
            validate.Regexp(
                r'^(?=.*[A-Za-z]{2,})(?=.*\d{2,})(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$',
                error=(
                    "A senha deve ter entre 6 e 10 caracteres, contendo pelo menos duas letras, "
                    "um caractere especial e dois números."
                )
            )
        ]
    )
    tipo = fields.String(
        required=True,
        validate=validate.OneOf(['avaliador', 'administrador'])
    )

class UsuarioService:
    def __init__(self):
        self.encryption = Encryption()

    # Converte os campos nome, email e tipo para letras minúsculas.
    def _normalize_data(self, data):
        if 'nome' in data:
            data['nome'] = data['nome'].lower()
        if 'email' in data:
            data['email'] = data['email'].lower()
        if 'tipo' in data:
            data['tipo'] = data['tipo'].lower()
        return data

    # Retorna todos os usuários cadastrados.
    def get_all(self):
        return UsuarioRepository.get_all()

    # Retorna um usuário pelo ID.
    def get_by_id(self, user_id):
        usuario = UsuarioRepository.get_by_id(user_id)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        return usuario

    # Retorna um usuário pelo e-mail.
    def get_by_email(self, email):
        usuario = UsuarioRepository.get_by_email(email.lower())
        if not usuario:
            raise Exception("Usuário não encontrado.")
        return usuario

    # Cria um novo usuário, garantindo e-mail único.
    def create_usuario(self, data):
        try:
            # Normaliza os dados para letras minúsculas
            normalized_data = self._normalize_data(data)

            # Verifica se o e-mail já está cadastrado
            if UsuarioRepository.get_by_email(normalized_data['email']):
                raise Exception("E-mail já está cadastrado.")

            usuario_data = UsuarioSchema().load(normalized_data)
            usuario_data['senha'] = self.encryption.encrypt(usuario_data['senha'])

            return UsuarioRepository.create(usuario_data)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Atualiza os dados de um usuário, garantindo e-mail único.
    def update(self, user_id, data):
        usuario = UsuarioRepository.get_by_id(user_id)
        if not usuario:
            raise Exception("Usuário não encontrado.")

        try:
            # Normaliza os dados para letras minúsculas
            normalized_data = self._normalize_data(data)

            # Se o e-mail está sendo alterado, verifica se já está em uso por outro usuário
            if 'email' in normalized_data and normalized_data['email'] != usuario.email:
                if UsuarioRepository.get_by_email(normalized_data['email']):
                    raise Exception("E-mail já está cadastrado.")

            updated_data = UsuarioSchema().load(normalized_data, partial=True)
            if 'senha' in updated_data:
                updated_data['senha'] = self.encryption.encrypt(updated_data['senha'])

            # Atualiza os atributos do usuário
            for key, value in updated_data.items():
                setattr(usuario, key, value)

            return UsuarioRepository.update(usuario)

        except ValidationError as err:
            raise Exception(f"Erro na validação: {err.messages}")

    # Deleta um usuário pelo ID.
    def delete(self, user_id):
        usuario = UsuarioRepository.get_by_id(user_id)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        UsuarioRepository.delete(user_id)
        return {"message": "Usuário deletado com sucesso."}

    # Autentica um usuário e gera um token JWT.
    def login(self, email, senha):
        usuario = UsuarioRepository.get_by_email(email.lower())
        if not usuario:
            raise Exception("Usuário não encontrado.")

        if not self.encryption.decrypt(usuario.senha) == senha:
            raise Exception("Senha inválida.")

        token = JWTManager.create_token({"id": str(usuario.id), "tipo": usuario.tipo})
        return {"token": token, "tipo": usuario.tipo}
