from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
import uuid
from datetime import datetime

class Projeto(db.Model):
    __tablename__ = 'projetos'
   
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo_projeto = db.Column(db.String(255), nullable=False)
    data_submissao = db.Column(db.Datetime, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    arquivo = db.Column(db.String(500), nullable=False)
    # Foreign key - Referenciando a chave primária da tabela Usuario
    avaliador_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), nullable=False)
    # Define o relacionamento para facilitar a navegação
    avaliador = db.relationship('Usuario', backref=db.backref('projetos', lazy=True))
    empresa_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), nullable=False)
    empresa = db.relationship('Usuario', backref=db.backref('projetos', lazy=True))
    
    __table_args__ = (
        CheckConstraint("tipo IN ('Avaliador', 'Administrador')", name='check_tipo'),
    )
    
    def __init__(self, titulo_projeto, status, arquivo, avaliador_nome, empresa_cnpj):
        
        self.titulo_projeto = titulo_projeto
        self.status = status
        self.arquivo = arquivo
        self.avaliador_nome = avaliador_nome
        self.empresa_cnpj = empresa_cnpj
        
    def __repr__(self):
        return f'<Projeto: {self.titulo_projeto}, Status: {self.status}, Arquivo: {self.arquivo}, Avaliador: {self.avaliador_nome}, Empresa: {self.empresa_cnpj}>'