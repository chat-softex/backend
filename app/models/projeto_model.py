# app/models/projeto_model.py:
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
    data_submissao = db.Column(db.TIMESTAMP, server_default=func.now())  
    status = db.Column(db.Enum('em avaliação', 'aprovado', 'reprovado', name='status_projeto'), nullable=False) # 
    arquivo = db.Column(db.String(500), nullable=False)

    # Foreign key - Referenciando a chave primária da tabela Usuario
    avaliador_id = db.Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='SET NULL')) 
    empresa_id = db.Column(UUID(as_uuid=True), ForeignKey('empresas.id', ondelete='CASCADE')) 
    
    # Relacionamento com Usuario e Empresa
    avaliador = relationship('Usuario', back_populates='projetos')
    empresa = relationship('Empresa', back_populates='projetos')

    # Relacionamento Um-para-Um com Avaliacao
    avaliacao = relationship('Avaliacao', back_populates='projeto', uselist=False)

    __table_args__ = (
        CheckConstraint("status IN ('em avaliação', 'aprovado', 'reprovado')", name='check_status'),
    )

    def __init__(self, titulo_projeto, status, arquivo, avaliador_id, empresa_id):
        
        self.titulo_projeto = titulo_projeto
        self.status = status
        self.arquivo = arquivo
        self.avaliador_id = avaliador_id
        self.empresa_id = empresa_id
        
    def __repr__(self):
        return f'<Projeto: {self.titulo_projeto}, Status: {self.status}, Arquivo: {self.arquivo}, Avaliador: {self.avaliador_id}, Empresa: {self.empresa_id}>'