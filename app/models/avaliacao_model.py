from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Review(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    projeto_id = db.Column(UUID(as_uuid=True), ForeignKey('projetos.id', ondelete='CASCADE'), unique=True)
    data_avaliacao = db.Column(db.TIMESTAMP, server_default=func.now())
    feedback_qualitativo = db.Column(db.Text, nullable=False)

    # Relacionamento com Projeto
    projeto = relationship('Project', back_populates='avaliacao', uselist=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "projeto_id": str(self.projeto_id),
            "data_avaliacao": self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            "feedback_qualitativo": self.feedback_qualitativo,
            "projeto": {
                "id": str(self.projeto.id),
                "titulo_projeto": self.projeto.titulo_projeto
            } if self.projeto else None  # inclui os detalhes do projeto (se disponível)
        }


    def __init__(self, projeto_id, feedback_qualitativo):
        self.projeto_id = projeto_id
        self.feedback_qualitativo = feedback_qualitativo

    def __repr__(self):
        return f'<Review: Projeto ID {self.projeto_id}, Feedback: {self.feedback_qualitativo[:20]}...>'
