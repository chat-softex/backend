# app/models/empresa_model.py:
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
    data_cadastro = db.Column(db.TIMESTAMP, server_default=func.now()) 
    
    projetos = relationship('Projeto', back_populates='empresa', cascade="all, delete-orphan")
    
    def __init__(self, nome_fantasia, cnpj, email):
        self.nome_fantasia = nome_fantasia.lower()
        self.cnpj = cnpj
        self.email = email.lower()
    
    def __repr__(self):
        return f'<Empresa: {self.nome_fantasia}, CNPJ: {self.cnpj}, Email: {self.email}>'