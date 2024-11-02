<<<<<<< HEAD
=======
# app/models/usuario_model.py:
# Importa a instância do banco de dados da aplicação (configurada em app/__init__.py).
from app import db

# Importa o tipo de dado UUID da extensão do PostgreSQL no SQLAlchemy, usado para gerar identificadores únicos para cada registro.
from sqlalchemy.dialects.postgresql import UUID

# Importa a classe que permite definir o relacionamento com outras tabelas.
from sqlalchemy.orm import relationship

# Importa a classe que permite definir restrições de verificação (check constraints) nas colunas da tabela.
from sqlalchemy import CheckConstraint

# Biblioteca padrão de Python para gerar UUIDs, usados como identificadores únicos.
import uuid

# Utilizado para gerar a data e hora atual no momento de cadastro dos usuários.
from sqlalchemy.sql import func


# Define uma classe que herda de db.Model, o que significa que ela representa uma tabela no banco de dados, neste caso, a tabela usuarios.
class Usuario(db.Model):
    # Especifica explicitamente o nome da tabela no banco de dados, que será "usuarios".
    __tablename__ = 'usuarios'

    # Chave primária (primary_key=True) da tabela, representada por um UUID. O valor padrão (default=uuid.uuid4) gera automaticamente um UUID ao criar um novo registro.
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Coluna do tipo String com um limite de 255 caracteres. É obrigatório (nullable=False).
    nome = db.Column(db.String(255), nullable=False)

    # Coluna do tipo String, também com um limite de 255 caracteres. O campo é obrigatório (nullable=False) e deve ser único no banco de dados (unique=True), garantindo que não existam dois usuários com o mesmo e-mail.
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Coluna que armazena a senha do usuário como uma string. O valor é obrigatório (nullable=False).
    senha = db.Column(db.String(255), nullable=False)

    # Coluna que define o tipo do usuário (ex: avaliador ou administrador). O valor é obrigatório (nullable=False).
    tipo = db.Column(db.Enum('avaliador', 'administrador', name='usuario_tipo'), nullable=False)

    # Coluna que armazena a data e hora do cadastro do usuário. O valor padrão é a data e hora atual (server_default=func.now()).
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now())

    # Relacionamento com Projetos (Um-para-Muitos)
    projetos = relationship('Projeto', back_populates='avaliador')

    # Define uma restrição na coluna tipo, garantindo que o valor só pode ser "avaliador" ou "administrador". Essa restrição garante integridade nos dados armazenados.
    __table_args__ = (
        CheckConstraint("tipo IN ('avaliador', 'administrador')", name='check_tipo'),
    )

    # Construtor da classe para inicializar um novo objeto Usuario com os valores de nome, email, senha, e tipo.
    def __init__(self, nome, email, senha, tipo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

    # Define como a instância da classe será representada quando impressa ou exibida no terminal. Ele retorna uma string que mostra o nome do usuário, o e-mail e o tipo. É útil para debugar.
    def __repr__(self):
        return f'<Usuario {self.nome}, Email: {self.email}, Tipo: {self.tipo}>'
>>>>>>> 8549260730c897cdf26c2777a2e23efd9c31b86f
