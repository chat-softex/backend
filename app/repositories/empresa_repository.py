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
