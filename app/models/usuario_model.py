# app/models/usuario_model.py
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
import uuid
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('avaliador', 'administrador', name='usuario_tipo'), nullable=False)
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now())

    # Relacionamento com Projetos (Um-para-Muitos)
    projetos = relationship('Project', back_populates='avaliador', lazy='dynamic')

    __table_args__ = (
        CheckConstraint("tipo IN ('avaliador', 'administrador')", name='check_tipo'),
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None
        }

    def __init__(self, nome, email, senha, tipo):
        self.nome = nome.lower()
        self.email = email.lower()
        self.senha = senha
        self.tipo = tipo.lower()

    def __repr__(self):
        return f'<Usuario: {self.nome}, Email: {self.email}, Tipo: {self.tipo}>'
