from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_fantasia = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now()) # nullable=False: usar essa condição na coluna da tabela fará com que o usuario seja obrigado a dogita esse valor visto que não aceitara valor nulo. Porém, esse valor não deverá ser informado pelo usuario. Ele será setado (gerado) automaticamente pelo banco de dados na hora que os dados forem salvos no bando de dados. Usar TIMESTAMP para armazenar um valor de data e hora. Define um valor padrão que será aplicado pelo servidor de banco de dados quando um novo registro for inserido. Isso significa que o valor não é gerado no lado do aplicativo (Python), mas diretamente no banco de dados. Usar server_default=func.now() - essa função (func.now()) invoca a função nativa do banco de dados que retorna a data e hora atuais. No caso do PostgreSQL, ela é equivalente à função NOW(), que retorna a data e hora do sistema do servidor do banco de dados no momento da inserção de um registro. O func é um objeto do SQLAlchemy que permite chamar funções SQL diretamente, como NOW().
    

    # não existe  "__table_args__ = (CheckConstraint("tipo IN ('Avaliador', 'Administrador')", name='check_tipo'),)" na tabela empresas (classe Empresa). "table_args__ = (CheckConstraint())""  está relacionada à definição de uma restrição de verificação de uma tabela. CheckConstraint é uma restrição que impõe uma condição de verificação sobre os valores que podem ser inseridos ou atualizados em uma coluna. 

    
    # relacionamento com tabela projetos (UM-para-Muitos). Uso de "cascade="all, delete-orphan"": aplica todas as operações em cascata. Quando a empresa é modificada ou deletada, as mudanças são automaticamente propagadas para seus projetos.". Essa configuração garante a consistência dos dados e o gerenciamento automático das entidades relacionadas (projetos) quando a entidade principal (empresa) é modificada ou removida.
    projetos = relationship('Projeto', back_populates='empresa', cascade="all, delete-orphan")
    
    def __init__(self, nome_fantasia, cnpj, email):
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj
        self.email = email
    
    def __repr__(self):
        return f'<Empresa: {self.nome_fantasia}, CNPJ: {self.cnpj}, Email: {self.email}>'