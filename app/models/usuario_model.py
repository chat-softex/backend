# app/models/usuario_model.py:
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
import uuid
from sqlalchemy.sql import func

class Usuario(db.Model):

    __tablename__ = 'usuarios'

  
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('avaliador', 'administrador', name='usuario_tipo'), nullable=False)
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now())

    # Relacionamento com Projetos (Um-para-Muitos)
    projetos = relationship('Projeto', back_populates='avaliador')

    __table_args__ = (
        CheckConstraint("tipo IN ('avaliador', 'administrador')", name='check_tipo'),
    )

    def __init__(self, nome, email, senha, tipo):
        self.nome = nome.lower()
        self.email = email.lower()
        self.senha = senha
        self.tipo = tipo.lower()

    def __repr__(self):
        return f'<Usuario: {self.nome}, Email: {self.email}, Tipo: {self.tipo}>'
