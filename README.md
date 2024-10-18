<h1>Chat Softex</h1>

<p align="center"> 
<img src="https://img.shields.io/static/v1?label=Python&message=3.x&color=3776AB&style=for-the-badge&logo=python"/> 
<img src="https://img.shields.io/static/v1?label=Flask&message=2.x&color=000000&style=for-the-badge&logo=flask"/> 
<img src="http://img.shields.io/static/v1?label=Draw.io&message=24.6.4&color=f08705&style=for-the-badge&logo=diagramsdotnet"/> 
<img src="http://img.shields.io/static/v1?label=Firebase&message=10.13.0&color=DD2C00&style=for-the-badge&logo=firebase"/> 
<img src="http://img.shields.io/static/v1?label=PostgreSQL&message=16&color=4169e1&style=for-the-badge&logo=postgresql&logoColor=f5f5f5"/> 
<img src="http://img.shields.io/static/v1?label=Workbench%20MySQL&message=8.0.38&color=4479a1&style=for-the-badge&logo=mysql&logoColor=f5f5f5"/> 
<img src="http://img.shields.io/static/v1?label=SQLAlchemy&message=2.x&color=2d3748&style=for-the-badge&logo=sqlalchemy"/> 
<img src="http://img.shields.io/static/v1?label=PyJWT&message=2.x&color=000000&style=for-the-badge&logo=jsonwebtokens"/> 
<img src="http://img.shields.io/static/v1?label=Cryptography&message=40.0.2&color=2b2b2b&style=for-the-badge&logo=cryptography"/> 
<img src="http://img.shields.io/static/v1?label=PyPDF2&message=3.x&color=blue&style=for-the-badge&logo=pypdf"/> 
<img src="http://img.shields.io/static/v1?label=Spacy&message=3.x&color=09A3D5&style=for-the-badge&logo=spacy"/> 
<img src="http://img.shields.io/static/v1?label=Python-DotEnv&message=1.x&color=ECD53F&style=for-the-badge&logo=dotenv"/> 
<img src="http://img.shields.io/static/v1?label=Flask-CORS&message=3.x&color=000000&style=for-the-badge&logo=cors"/> 
<img src="http://img.shields.io/static/v1?label=Postman&message=10.16.2&color=FF6C37&style=for-the-badge&logo=postman"/> 
<img src="http://img.shields.io/static/v1?label=Git&message=2.45.2&color=f05032&style=for-the-badge&logo=git"/> 
<img src="http://img.shields.io/static/v1?label=GitHub&message=2024&color=181717&style=for-the-badge&logo=github"/> 
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=yellow&style=for-the-badge"/> 
<img src="http://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/> 
</p>

> Status do Projeto: :heavy_check_mark: (concluido) | :warning: (em desenvolvimento) | :x: (não iniciada)

### Tópicos 

:small_blue_diamond: [Arquitetura do Backend](#arquitetura-do-backend-triangular_ruler-straight_ruler) :heavy_check_mark:

:small_blue_diamond: [Rotas - EndPoints](#rotas---endpoints-arrows_clockwise) :x:

:small_blue_diamond: [Instalação das Dependências](#Instalação-das-depedências-arrow_down_small)

:small_blue_diamond: [Iniciação e migration Database](#Iniciação-e-migration-Database-file_folder)

:small_blue_diamond: [Executar App](#executar-app-arrow_forward)

...

## Arquitetura do Backend :triangular_ruler: :straight_ruler:

**Diagrama:**

<img src="https://github.com/chat-softex/.github/blob/main/profile/diagrama_arquitetura_software_gestao_projetos_inovacao.png" alt="Diagrama de Arquitetura de Software">

... 


```plaintext
sistema_assistente_de_avaliacao_de_projetos_de_inovacao/
│
├── app/
│   ├── __init__.py                     # Inicialização do app Flask e configuração do SQLAlchemy 
|   |
│   ├── models/                         # Definições das tabelas - Modelos do SQLAlchemy (ORM)
|   |   ├── empresa_model.py            # Modelo para empresas
│   │   ├── projeto_model.py            # Modelo para projetos
│   │   ├── usuario_model.py            # Modelo para usuários
│   │   └── avaliacao_model.py          # Modelo para avaliações
|   |
│   ├── routes/                         # Definição das rotas da API (CRUD para projetos, avaliações, usuários)
|   |   ├── empresa_routes.py           # Rotas para empresas
│   │   ├── projeto_routes.py           # Rotas para projetos
│   │   ├── usuario_routes.py           # Rotas para usuários
│   │   └── avaliacao_routes.py         # Rotas para avaliações
|   |
│   ├── middlewares/                    # Middleware de segurança e autenticação (ex: JWT, CORS)
│   │   ├── auth.py                     # Middleware JWT para autenticação
|   |   └── cors_middleware.py
|   |
│   ├── utils/                          # Funções utilitárias (criptografia, JWT, etc.)
│   │   ├── encryption.py               # Funções para criptografia de arquivos
│   │   ├── jwt_manager.py              # Gerenciamento de tokens JWT
│   │   └── file_utils.py               # Funções de upload e download de arquivos (firebase)
|   |
│   ├── controllers/                    # Controladores que recebem e processam as requisições HTTP
|   |   ├── empresa_controller.py       # Lógica de CRUD para empresas
│   │   ├── projeto_controller.py       # Lógica de CRUD para projetos
│   │   ├── usuario_controller.py       # Lógica de CRUD para usuários
│   │   └── avaliacao_controller.py     # Lógica para avaliação e feedback
|   |
│   ├── services/                       # Validações e regras de negócio
│   │   ├── ia_service.py               # Integração com IA (API ChatGPT)
│   │   ├── firebase_service.py         # Upload/Download de PDFs no Firebase
|   |   ├── empresa_controller.py       # Validações e regras de negócio para empresas
│   │   ├── projeto_service.py          # Validações e regras de negócio para projetos
│   │   ├── usuario_service.py          # Validações e regras de negócio para usuários
│   │   └── avaliacao_service.py        # Regras de negócio para avaliações
|   |
│   ├── repositories/                   # Operações de acesso ao banco de dados
|   |   ├── empresa_controller.py       # Métodos para interagir com a tabela de empresas
│   │   ├── projeto_repository.py       # Métodos para interagir com a tabela de projetos
│   │   ├── usuario_repository.py       # Métodos para interagir com a tabela de usuários
│   │   └── avaliacao_repository.py     # Métodos para interagir com a tabela de avaliações
|   |
│   └── config/                         # Configurações gerais do Flask e do banco de dados
|       └── config.py
│
├── migrations/                         # Migrações de banco de dados
│
|   
├── requirements.txt                    # Dependências do projeto
|   
├── .env                                # Variáveis de ambiente sensíveis(configurações de acesso-Firebase,JWT,DB)
|   
├── app.py                              # Arquivo principal da aplicação Flask
|   
└── README.md                           # Documentação
```

**Descrição:** :x:

1. **models/:** Define as tabelas e entidades do banco de dados usando SQLAlchemy.

2. **routes/:** Define as rotas da API para cada entidade do sistema (projetos, usuários, avaliações).

3. **controllers/:** Implementam a lógica de controle, recebendo as requisições HTTP e invocando os serviços.

4. **services/:** Camada de lógica de negócio, validações e processamento e integrações com serviços externos (IA, Firebase).

5. **repositories/:** Responsável por interagir com o banco de dados através do ORM SQLAlchemy.

6. **middleware/:** Implementa segurança e autenticação.

7. **utils/:** Funções auxiliares, como criptografia e gerenciamento de tokens.

8. **config/:** Configurações gerais da aplicação.

9. **migrations/:** Contém as migrações de banco de dados, responsáveis por criar, alterar e manter as tabelas no PostgreSQL.

10. **requirements.txt:** Lista de todas as dependências e bibliotecas necessárias para o projeto (ex.: Flask, SQLAlchemy, Firebase SDK).

11. **.env:** Arquivo de variáveis de ambiente sensíveis, como chaves de API, credenciais do Firebase, configurações de JWT, entre outros.

12. **app.py:** Arquivo principal que inicializa e executa a aplicação Flask.

13. **README.md:** Documentação do projeto, instruções de configuração, execução e detalhes de cada parte do sistema.


## Rotas - EndPoints :arrows_clockwise:

1. **Usuarios:** :x:
   - GET /users: Retorna todos os usuários.
   - GET /users/{id}: Retorna um usuário específico por ID.
   - POST /users: Cadastra um novo usuário.
   - PUT /users/{id}: Atualiza os dados de um usuário por ID.
   - DELETE /users/{id}: Deleta um usuário por ID.
   - POST /users/login: Autentica um usuário e retorna o token JWT.


2. **Projetos:** :x:
   - GET /projects: Retorna todos os projetos.
   - GET /projects/{id}: Retorna um projeto específico por ID.
   - POST /projects: Cria um novo projeto (upload de um projeto).
   - PUT /projects/{id}: Atualiza os dados de um projeto por ID.
   - DELETE /projects/{id}: Deleta um projeto por ID.
   - PATCH /projects/{id}/status: Atualiza o status de um projeto ('Em avaliação', 'Aprovado', 'Reprovado').



3. **Avaliações:** :x:
   - POST /reviews: Cria uma avaliação para um projeto específico.
   - GET /reviews/projects: Retorna a avaliação de todos os projetos.
   - GET /reviews/{project_id}: Retorna a avaliação de um projeto específico.
   - PUT /reviews/{id}: Atualiza uma avaliação por ID.
   - DELETE /reviews/{id}: Deleta uma avaliação por ID.


## Instalação das depedências :arrow_down_small:

```bash
$ pip install -r requirements.txt

```


## Iniciação e migration Database :file_folder:

```bash
$ flask db init
$ flask db migrate -m "Initial migration"
$ flask db upgrade

```

## Executar app :arrow_forward:

**development:**
```bash
$ flask run

```

```bash
Running on http://localhost:5000/

```

...  


## Licença 

The [MIT License]() (MIT)

Copyright :copyright: 2024 - Chat Softex
