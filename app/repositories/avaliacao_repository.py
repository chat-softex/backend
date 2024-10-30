from app.models.avaliacao_model import Avaliacao
from app.models.projeto_model import Projeto
from sqlalchemy.orm import joinedload
from app import db

class AvaliacaoRepository:

    @staticmethod
    def get_all():
        return db.session.query(Avaliacao).options(
            joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
        ).all()  
        
    @staticmethod
    def get_by_id(id):
        return db.session.query(Avaliacao).filter_by(id=id).options(
            joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
        ).first()
    
    @staticmethod
    def create(avaliacao):
        db.session.add(avaliacao)
        db.session.commit()
        return avaliacao

    @staticmethod
    def update(avaliacao):
        db.session.commit()
        return avaliacao

    @staticmethod
    def delete(id):
        avaliacao = db.session.query(Avaliacao).get(id)
        if avaliacao:
            db.session.delete(avaliacao)
            db.session.commit()
        else:
            raise Exception("Avaliação não existe.")    