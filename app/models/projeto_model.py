from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.sql import func
import uuid

class Projeto(db.Model):
    __tablename__ = 'projetos'
   
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo_projeto = db.Column(db.String(255), nullable=False)
    data_submissao = db.Column(db.TIMESTAMP, server_default=func.now())  # nullable=False: usar essa condição na coluna da tabela fará com que o usuario seja obrigado a dogita esse valor visto que não aceitara valor nulo. Porém, esse valor não deverá ser informado pelo usuario. Ele será setado (gerado) automaticamente pelo banco de dados na hora que os dados forem salvos no bando de dados. Usar TIMESTAMP para armazenar um valor de data e hora. Define um valor padrão que será aplicado pelo servidor de banco de dados quando um novo registro for inserido. Isso significa que o valor não é gerado no lado do aplicativo (Python), mas diretamente no banco de dados. Usar server_default=func.now() - essa função (func.now()) invoca a função nativa do banco de dados que retorna a data e hora atuais. No caso do PostgreSQL, ela é equivalente à função NOW(), que retorna a data e hora do sistema do servidor do banco de dados no momento da inserção de um registro. O func é um objeto do SQLAlchemy que permite chamar funções SQL diretamente, como NOW().

    status = db.Column(db.Enum('Em avaliação', 'Aprovado', 'Reprovado', name='status_projeto'), nullable=False) # Coluna define Status do projeto que pode ser 'Em avaliação', 'Aprovado' ou 'Reprovado'

    arquivo = db.Column(db.String(500), nullable=False)

    # Foreign key - Referenciando a chave primária da tabela Usuario
    avaliador_id = db.Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='SET NULL')) # usar "ondelete='SET NULL'"" - define o comportamento de exclusão em cascata quando o registro na tabela usuarios é excluído. Ou seja, o que deve acontecer com o registro na tabela atual (projetos) quando o usuário associado (o avaliador) for excluído.

    empresa_id = db.Column(UUID(as_uuid=True), ForeignKey('empresas.id', ondelete='CASCADE')) # ondelete='CASCADE' - define o comportamento de exclusão em cascata. Especificamente, ele indica que se um registro na tabela empresas for excluído, todos os registros na tabela atual (por exemplo, projetos) que referenciam essa empresa serão automaticamente excluídos. Ou seja, a exclusão de uma empresa aciona a exclusão de todos os registros relacionados.
    
    
    # Relacionamento com Usuario e Empresa
    avaliador = relationship('Usuario', back_populates='projetos')
    
    empresa = relationship('Empresa', back_populates='projetos')

    
    #  não existe "__table_args__ = (CheckConstraint("tipo IN ('Avaliador', 'Administrador')", name='check_tipo'),)"". A tabela projetos não tem a coluna tipo. A coluna correta é status. E não existe 'Avaliador', 'Administrador' em status. Em status é 'Em avaliação', 'Aprovado', 'Reprovado'.
    __table_args__ = (
        CheckConstraint("status IN ('Em avaliação', 'Aprovado', 'Reprovado')", name='check_status'),
    )

    
    # os relacionamentos entre a tabela projetos e empresas são atraves do id (avaliador_id e empresa_id) e não entre nome do avalidor e o cnpj da empresa. No init são carregados os atributos da tabela projetos. Observem que nome do avaliador e cnjp da empresa não são atributos da tabela projeto. O que vai ser retornado para o usuario atraves de "select" e "join" (como nome do avaliador, nome da empresa) são operações de manipilação do banco de dados que são realizadas na camada repositories e não em models. O models são apenas a defifinção das tabelas no banco de dados, ou seja, entidades, atributos, relacionamentos e restrições de segurança e integridade das tabelas.
    def __init__(self, titulo_projeto, status, arquivo, avaliador_id, empresa_id):
        
        self.titulo_projeto = titulo_projeto
        self.status = status
        self.arquivo = arquivo
        self.avaliador_id = avaliador_id
        self.empresa_id = empresa_id
        
    def __repr__(self):
        return f'<Projeto: {self.titulo_projeto}, Status: {self.status}, Arquivo: {self.arquivo}, Avaliador: {self.avaliador_id}, Empresa: {self.empresa_id}>'