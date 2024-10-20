# Importa o modelo Projeto, que representa a entidade 'Projeto' no banco de dados.
from app.models.projeto_model import Projeto
# Importa a instância do banco de dados para gerenciar conexões e transações usando SQLAlchemy.
from app import db
# Importa joinedload para carregar relacionamentos em consultas
from sqlalchemy.orm import joinedload

# Repositório que encapsula toda a lógica de acesso e manipulação de dados relacionados ao modelo Projeto.
# Fornece métodos para operações CRUD (Create, Read, Update e Delete).
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
    def get_by_id(projeto_id):
        return db.session.query(Projeto).options(
            joinedload(Projeto.avaliador),
            joinedload(Projeto.empresa),
            joinedload(Projeto.avaliacao)
        ).filter(Projeto.id == projeto_id).first()
    
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
    def delete(projeto_id):
        projeto = Projeto.query.get(projeto_id)
        if projeto:
            db.session.delete(projeto)
            db.session.commit()
