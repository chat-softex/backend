from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
import uuid
from datetime import datetime

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    projeto_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projetos.id'), nullable=False, unique=True)  # FK para Projetos, garantindo que cada projeto tenha apenas uma avaliação
    data_avaliacao = db.Column(db.TIMESTAMP, server_default=func.now())  # Data da avaliação com valor padrão
    feedback_qualitativo = db.Column(db.Text, nullable=False)  # Feedback gerado pela IA

    # Relacionamento com a tabela Projeto
    projeto = db.relationship('Projeto', backref=db.backref('avaliacao', uselist=False))  # Define um relacionamento um-para-um
    
    

    def __init__(self, projeto_id, feedback_qualitativo):
        self.projeto_id = projeto_id
        self.feedback_qualitativo = feedback_qualitativo

    def __repr__(self):
        return f'<Avaliacao: Projeto ID {self.projeto_id}, Feedback: {self.feedback_qualitativo[:20]}...>'