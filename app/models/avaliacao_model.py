# app/models/avaliacao_model.py:
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    projeto_id = db.Column(UUID(as_uuid=True), ForeignKey('projetos.id', ondelete='CASCADE'), unique=True)  # usar "ondelete='CASCADE'"" para definir o comportamento de exclusão em cascata. Especificamente, ele indica que se um registro na tabela empresas for excluído, todos os registros na tabela atual (por exemplo, projetos) que referenciam essa empresa serão automaticamente excluídos. Ou seja, a exclusão de uma empresa aciona a exclusão de todos os registros relacionados.

    data_avaliacao = db.Column(db.TIMESTAMP, server_default=func.now())# Data da avaliação com valor padrão
    
    feedback_qualitativo = db.Column(db.Text, nullable=False)  # Feedback gerado pela IA

    # Relacionamento com Projeto (Um-para-Um)
    projeto = relationship('Projeto', back_populates='avaliacao', uselist=False) # Usar back_populates para ter maior controle dos relacionamentos entre as tabelas
    

    def __init__(self, projeto_id, feedback_qualitativo):
        self.projeto_id = projeto_id
        self.feedback_qualitativo = feedback_qualitativo

    def __repr__(self):
        return f'<Projeto: {self.projeto_id}, Feedback Qualitativo: {self.feedback_qualitativo[:20]}...>'