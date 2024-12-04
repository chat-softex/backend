from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.sql import func
import uuid


class Project(db.Model):
    __tablename__ = 'projetos'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    titulo_projeto = db.Column(db.String(255), nullable=False)
    data_submissao = db.Column(db.TIMESTAMP, server_default=func.now())
    status = db.Column(db.Enum('em avaliação', 'aprovado', 'reprovado', name='status_projeto'), nullable=False)
    arquivo = db.Column(db.String(500), nullable=False)

    # Foreign keys
    avaliador_id = db.Column(UUID(as_uuid=True), ForeignKey('usuarios.id', ondelete='SET NULL'))
    empresa_id = db.Column(UUID(as_uuid=True), ForeignKey('empresas.id', ondelete='CASCADE'))

    # Relacionamentos
    avaliador = relationship('User', back_populates='projetos')
    empresa = relationship('Company', back_populates='projetos')
    avaliacao = relationship('Review', back_populates='projeto', uselist=False)

    __table_args__ = (
        CheckConstraint("status IN ('em avaliação', 'aprovado', 'reprovado')", name='check_status'),
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "titulo_projeto": self.titulo_projeto,
            "data_submissao": self.data_submissao.isoformat() if self.data_submissao else None,
            "status": self.status,
            "arquivo": self.arquivo,
            "avaliador": {
                "id": str(self.avaliador.id),
                "nome": self.avaliador.nome
            } if self.avaliador else None,  # incluir os detalhes do avaliador
            "empresa": {
                "id": str(self.empresa.id),
                "nome_fantasia": self.empresa.nome_fantasia
            } if self.empresa else None,  # dados basicos da empresa
            "avaliacao": self.avaliacao.to_dict() if self.avaliacao else None  # incluir avaliação associada
        }


    def __init__(self, titulo_projeto, status, arquivo, avaliador_id, empresa_id):
        self.titulo_projeto = titulo_projeto.lower()
        self.status = status.lower()
        self.arquivo = arquivo
        self.avaliador_id = avaliador_id
        self.empresa_id = empresa_id

    def __repr__(self):
        return f'<Projeto: {self.titulo_projeto}, Status: {self.status}>'
