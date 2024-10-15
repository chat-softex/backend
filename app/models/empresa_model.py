from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
import uuid
from datetime import datetime

class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_fantasia_empresa = db.Column(db.String(255), nullable=False)
    cnpj_empresa = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.Datetime, nullable=False)
    
    table_args__ = (
        CheckConstraint("tipo IN ('Avaliador', 'Administrador')", name='check_tipo'),
    )
    
    def __init__(self, nome_fantasia_empresa, cnpj_empresa, email):
        self.nome_fantasia_empresa = nome_fantasia_empresa
        self.cnpj_empresa = cnpj_empresa
        self.email = email
        #self.data_cadastro = datetime.now()
    
    def __repr__(self):
        return f'<Empresa: {self.nome_fantasia_empresa}, CNPJ: {self.cnpj_empresa}, Email: {self.email}>'