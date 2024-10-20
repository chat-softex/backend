# Importa o modelo Empresa da pasta models, que mapeia a tabela 'empresas' no banco de dados
from app.models.empresa_model import Empresa

# Importa a instância do banco de dados, que gerencia as conexões e transações via SQLAlchemy
from app import db

# A classe EmpresaRepository agrupa todos os métodos relacionados à manipulação de dados da entidade Empresa.
## Utiliza SQLAlchemy para realizar operações CRUD no banco de dados.
class EmpresaRepository:
   
    # Método estático def get_all() - retorna todas as empresas registradas no banco de dados. Dica: utilize método all() da consulta ORM
    @staticmethod
    def get_all():
        
    # Método estático def get_by_id(empresa_id) - Retorna uma empresa específica pelo seu ID. Dica: utilize método get() da consulta ORM 
    @staticmethod
    def get_by_id(empresa_id):
        
    # Método estático def get_by_cnpj(cnpj) - Retorna uma empresa específica pelo seu cnpj. Dica: utilize método filter_by() para filtrar por uma coluna específica (neste caso, cnpj) e método first() para retornar apenas o primeiro resultado  da consulta ORM.
    @staticmethod
    def get_by_cnpj(cnpj):
        

    # Método estático def create(empresa) - Adiciona uma nova empresa ao banco de dados. Dica: utilize .session.add() para adicionar o objeto empresa à sessão atual e .session.commit() para gravar a transação no banco de dados e retorne empresa.
    @staticmethod
    def create(empresa):
        
    
    # Método estático def update(empresa) - Atualiza uma empresa no banco de dados. Dica: utilize .session.commit() grava essas mudanças no banco de dados e e retorne empresa.
    @staticmethod
    def update(empresa):
        

    # Método estático def delete(empresa_id) - Remove uma empresa com o ID fornecido do banco de dados. Dica: utilize método get() para buscar a empresa, .session.delete() para deletar e .session.commit() para finalizar a sessão.
    @staticmethod
    def delete(empresa_id):
        
