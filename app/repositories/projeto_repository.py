from app.models.projeto_model import Projeto
from app import db
from sqlalchemy.orm import joinedload

class ProjetoRepository:

    # Realiza uma consulta para retornar todos os registros da tabela 'projetos' com avaliadores, empresas e avaliações.
    @staticmethod
    def get_all():
        return db.session.query(Projeto).options(
            joinedload(Projeto.avaliador),   # Carrega o avaliador relacionado
            joinedload(Projeto.empresa),     # Carrega a empresa relacionada
            joinedload(Projeto.avaliacao)    # Carrega a avaliação relacionada (1:1)
        ).all()


    # Retorna um projeto específico pelo ID com seus relacionamentos..
    @staticmethod
    def get_by_id(id):
        return db.session.query(Projeto).filter_by(id=id).options(
            joinedload(Projeto.avaliador),
            joinedload(Projeto.empresa),
            joinedload(Projeto.avaliacao)
        ).first()
    
    # Adiciona um novo projeto ao banco de dados e retorna Objeto Projeto recém-criado.
    @staticmethod
    def create(projeto):
        db.session.add(projeto)
        db.session.commit()
        return projeto

    # Atualiza os dados de um projeto existente e retorna Objeto Projeto com os dados atualizados.
    @staticmethod
    def update(projeto):
        db.session.commit()
        return projeto

    # Remove um projeto do banco de dados com base no seu ID.
    @staticmethod
    def delete(id):
        projeto = Projeto.query.get(id)
        if projeto:
            db.session.delete(projeto)
            db.session.commit()
