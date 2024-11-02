# Importa os modelos ORM que representam as tabelas avaliacoes e projetos.
from app.models.avaliacao_model import Avaliacao
from app.models.projeto_model import Projeto

# Importa joinedload. O método joinedload permite o carregamento antecipado dos relacionamentos, evitando múltiplas consultas e melhorando a performance ao carregar dados relacionados (como Avaliacao com Projeto e o avaliador do projeto
from sqlalchemy.orm import joinedload

# Importa a instância do banco de dados, que gerencia as conexões e transações via SQLAlchemy
from app import db

# A classe AvaliacaoRepository agrupa todas as operações CRUD e consultas relacionadas à entidade Avaliacao.
class AvaliacaoRepository:

    # Método estático def get_all() - retorna todas as avaliações armazenadas no banco de dados, juntamente com os projetos e seus avaliadores. Dica: utilize método all() da consulta ORM e o método joinedload para carregar o Projeto associado a cada avaliação e carrega também o avaliador do projeto em uma única consulta.
    @staticmethod
    def get_all():
        return db.session.query(Avaliacao).options(
            joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
        ).all()  
        # CORREÇÃO: ao inves de joinedload(Avaliacao.usuarios), o correto é joinedload(Projeto.avaliador)
        # avaliacao ñ possui uma relação direta com usuarios. A relação é indireta por meio da tabela Projeto (ou seja, Avaliacao → Projeto → Avaliador).
        # O objetivo era:
        # Carregar todas as avaliações do banco de dados.
        # Trazer também os projetos associados a essas avaliações.
        # Incluir o avaliador responsável pelo projeto, sem fazer múltiplas consultas separadas (ou seja, usando carregamento antecipado para otimizar a performance).

    # Método estático def get_by_id(id) - Retorna uma avaliação específica pelo seu ID, incluindo o projeto associado e o avaliador do projeto. Dica: utilize método filter_by() para filtrar por uma coluna específica (neste caso, id) e método first() para retornar apenas o primeiro resultado  da consulta ORM e e o método joinedload para carregar o Projeto associado a avaliação e carrega também o avaliador do projeto em uma única consulta.
    @staticmethod
    def get_by_id(id):
        return db.session.query(Avaliacao).filter_by(id=id).options(
            joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
        ).first()
    # CORREÇÃO: ao inves de joinedload(Avaliacao.usuarios), o correto é joinedload(Projeto.avaliador)
    # avaliacao ñ possui uma relação direta com usuarios. A relação é indireta por meio da tabela Projeto (ou seja, Avaliacao → Projeto → Avaliador).
    # O objetivo era:
    # Carregar todas as avaliações do banco de dados.
    # Trazer também os projetos associados a essas avaliações.
    # Incluir o avaliador responsável pelo projeto, sem fazer múltiplas consultas separadas (ou seja, usando carregamento antecipado para otimizar a performance).

    @staticmethod
    def get_by_projeto_id(projeto_id):
        return db.session.query(Avaliacao).filter_by(projeto_id=projeto_id).options(
            joinedload(Avaliacao.projeto).joinedload(Projeto.avaliador)
        ).first()
    
    # Método estático def create(avaliacao): - Adiciona uma nova avaliacao ao banco de dados. Dica: utilize .session.add() para adicionar o objeto avaliacao à sessão atual e .session.commit() para gravar a transação no banco de dados e retorne avaliacao.
    @staticmethod
    def create(avaliacao):
        db.session.add(avaliacao)
        db.session.commit()
        return avaliacao

    # Método estático def update(avaliacao) - Atualiza uma avaliacao no banco de dados. Dica: utilize .session.commit() grava essas mudanças no banco de dados e retorne avaliacao.
    @staticmethod
    def update(avaliacao):
        db.session.commit()
        return avaliacao

    # Método estático def delete(id) - Remove uma avaliacao com o ID fornecido do banco de dados. Dica: utilize método get() para buscar a avaliacao, .session.delete() para deletar e .session.commit() para finalizar a sessão.
    @staticmethod
    def delete(id):
        avaliacao = db.session.query(Avaliacao).get(id)
        if avaliacao:
            db.session.delete(avaliacao)
            db.session.commit()
        else:
            raise Exception("Avaliação não existe.")    