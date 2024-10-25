<<<<<<< HEAD
# Importa o modelo Empresa, que representa a entidade 'Empresa' no banco de dados.
from app.models.empresa_model import Empresa
# Importa a instância do banco de dados para gerenciar conexões e transações usando SQLAlchemy.
from app import db

# Classe que encapsula todas as operações CRUD (Create, Read, Update, Delete) para a entidade Empresa
class EmpresaRepository:

    # Retorna todos as Empresas cadastradas no banco de dados.
    @staticmethod
    def get_all():
        return Empresa.query.all()

    # Retorna a Empresa específica pelo ID.
    @staticmethod
    def get_by_id(id):
        return Empresa.query.get(id)

    # Retorna a Empresa específica pelo nome fantasia.
    @staticmethod
    def get_by_nome_fantasia(nome_fantasia):
        return Empresa.query.filter_by(nome_fantasia_empresa=nome_fantasia).first()
    
    # Retorna a Empresa específica pelo CNPJ.
    @staticmethod
    def get_by_cnpj(cnpj):
        return Empresa.query.filter_by(cnpj_empresa=cnpj).first()
    
    # Retorna a Empresa específica pelo email.
    @staticmethod
    def get_by_email_empresa(email_empresa):
        return Empresa.query.filter_by(email=email_empresa).first()
    
    # Adiciona uma nova Empresa ao banco de dados.
    @staticmethod
    def create(empresa):
        db.session.add(empresa)
        db.session.commit()
        return empresa

    # Atualiza uma Empresa existente no banco de dados.
    @staticmethod
    def update(empresa):
        db.session.commit()
        return empresa

    # Remove uma Empresa do banco de dados com base no ID.
    @staticmethod
    def delete(id):
        empresa = Empresa.query.get(id)
        if empresa:
            db.session.delete(empresa)
            db.session.commit()
        else:
            raise Exception("Empresa não existe.")
=======
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
        
>>>>>>> 66a7f68436d3663dec084f4830cfa4ba85942850
