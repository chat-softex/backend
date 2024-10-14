# importa a instância do banco de dados da aplicação (configurada em app/__init__.py). Isso permite utilizar os recursos do SQLAlchemy.
from app import db
# importa o tipo de dado UUID da extensão do PostgreSQL no SQLAlchemy, usado para gerar identificadores únicos para cada registro.
from sqlalchemy.dialects.postgresql import UUID
# importa a classe que permite definir restrições de verificação (check constraints) nas colunas da tabela.
from sqlalchemy import CheckConstraint
# biblioteca padrão de Python para gerar UUIDs, usados como identificadores únicos.
import uuid
# utilizado para gerar a data e hora atual no momento de cadastro dos usuários.
from datetime import datetime

# define uma classe que herda de db.Model, o que significa que ela representa uma tabela no banco de dados, neste caso, a tabela usuarios.
class Usuario(db.Model):
    # especifica explicitamente o nome da tabela no banco de dados, que será "usuarios".
    __tablename__ = 'usuarios'

    # chave primária (primary_key=True) da tabela, representada por um UUID. O valor padrão (default=uuid.uuid4) gera automaticamente um UUID ao criar um novo registro.
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Coluna do tipo String com um limite de 255 caracteres. É obrigatório (nullable=False).
    nome = db.Column(db.String(255), nullable=False)

    # Coluna do tipo String, também com um limite de 255 caracteres. O campo é obrigatório (nullable=False) e deve ser único no banco de dados (unique=True), garantindo que não existam dois usuários com o mesmo e-mail.
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Coluna que armazena a senha do usuário como uma string. O valor é obrigatório (nullable=False).
    senha = db.Column(db.String(255), nullable=False)

    # Coluna que define o tipo do usuário (ex: Avaliador ou Administrador). O valor é obrigatório (nullable=False).
    tipo = db.Column(db.String(50), nullable=False)

    # Coluna que armazena a data e hora do cadastro do usuário. O valor padrão é a data e hora atual (default=datetime.utcnow).
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Define uma restrição na coluna tipo, garantindo que o valor só pode ser "Avaliador" ou "Administrador". Essa restrição garante integridade nos dados armazenados.
    __table_args__ = (
        CheckConstraint("tipo IN ('Avaliador', 'Administrador')", name='check_tipo'),
    )

    #  __init__ é o construtor da classe e permite que irá inicializar um novo objeto Usuario com os valores de nome, email, senha, e tipo (apenas os dados setados pelo usuário).
    def __init__(self, nome, email, senha, tipo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo


    # __repr__ é o método que define como a instância da classe será representada quando impressa ou exibida no terminal. Ele retorna uma string que mostra o nome do usuário, o e-mail e o tipo. É util para debugar
    def __repr__(self):
        return f'<Usuario {self.nome}, Email: {self.email}, Tipo: {self.tipo}>'

