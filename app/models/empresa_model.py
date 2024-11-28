# app/models/empresa_model.py
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Company(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    nome_fantasia = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now())

    # Relacionamento com Projetos
    projetos = relationship('Project', back_populates='empresa', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome_fantasia": self.nome_fantasia,
            "cnpj": self.cnpj,
            "email": self.email,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None,
            "projetos": [
                {"id": str(projeto.id), "titulo_projeto": projeto.titulo_projeto}
                for projeto in self.projetos
            ]  # lista de IDs e títulos dos projetos associados
        }



    def __init__(self, nome_fantasia, cnpj, email):
        self.nome_fantasia = nome_fantasia.lower()
        self.cnpj = cnpj
        self.email = email.lower()

    def __repr__(self):
        return f'<Empresa: {self.nome_fantasia}, CNPJ: {self.cnpj}>'
