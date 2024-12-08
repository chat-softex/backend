# ChatSoftex

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

:small_blue_diamond: [Rotas - EndPoints](#rotas---endpoints-arrows_clockwise)  :heavy_check_mark:

:small_blue_diamond: [Clonar Repositório](#clonar-repositório-file_folder-arrow_right-file_folder) 

:small_blue_diamond: [Contribuições](#contribuições-technologist) 

:small_blue_diamond: [Criar e ativar ambiente virtual](#criar-e-ativar-ambiente-virtual-white_check_mark)

:small_blue_diamond: [Configurar as variáveis de ambiente](#configurar-as-variáveis-de-ambiente-white_check_mark)

:small_blue_diamond: [Instalação das Dependências](#instalação-das-depedências-arrow_down_small)

:small_blue_diamond: [Iniciação e migration Database](#iniciação-e-migration-database-file_folder)

:small_blue_diamond: [Executar App](#executar-app-arrow_forward)

---

## Arquitetura do Backend :triangular_ruler: :straight_ruler:

**Diagrama:**

<img src="https://github.com/chat-softex/.github/blob/main/doc/diagrama_arquitetura_software_ChatSoftex.drawio.png" alt="Diagrama de Arquitetura de Software">

--- 

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
│   │   ├── auth.py                     # Middlewares para proteger rotas com autenticação JWT e verificar permissões específicas de usuários
|   |   └── cors_middleware.py          # Middleware para habilitar CORS, permitindo que a aplicação receba requisições de origens diferentes 
|   |
│   ├── utils/                          # Funções utilitárias (criptografia, JWT, etc.)
│   │   ├── encryption.py               # Funções para criptografia de arquivos
│   │   ├── jwt_manager.py              # Gerencia a criação e decodificação de tokens JWT, usados para autenticação de usuários
│   │   ├── file_utils.py               # Utilitário para manipulação de arquivos PDF e upload para o Firebase
|   |   └── text_extractor.py           # Extração de texto de arquivos PDF, DOC e DOCS
|   |
│   ├── controllers/                    # Controladores que recebem e processam as requisições HTTP
|   |   ├── empresa_controller.py       # Requisições HTTP e invocando os serviços para empresas
│   │   ├── projeto_controller.py       # Requisições HTTP e invocando os serviços para projetos
│   │   ├── usuario_controller.py       # Requisições HTTP e invocando os serviços para usuários
│   │   └── avaliacao_controller.py     # Requisições HTTP e invocando os serviços para avaliação e feedback
|   |
│   ├── validators/                    # Validação de dados de entrada como formatos, tipos, e outras restrições básicas através das bibliotecas marshmallow e validate-docbr
|   |   ├── empresa_validator.py       # Validação de dados de entrada de  empresas
│   │   ├── projeto_validator.py       # Validação de dados de entrada de projetos
│   │   ├── usuario_validator.py       # Validação de dados de entrada de usuários
│   │   └── avaliacao_validator.py     # Validação de dados de entrada de avaliação e feedback
|   |
|   |
│   ├── erros/                         # Exceções específicas da aplicação e classes de erro personalizadas para lidar com erros
│   │   ├── custom_errors.py           # Exceções personalizadas para erros comuns que podem ocorrer em uma aplicação
│   │   └── error_handler.py           # Centraliza o tratamento de erros na aplicação
|   |
│   ├── services/                       # Validações das regras de negócio
│   │   ├── ia_service.py               # Integração com IA (API OpenAI - ChatGPT)
│   │   ├── firebase_service.py         # Configura e implementa o serviço FirebaseService, que interage com o Firebase Storage para upload e download de arquivos.
|   |   ├── empresa_service.py          # Validações das regras de negócio para empresas
│   │   ├── projeto_service.py          # Validações das regras de negócio para projetos
│   │   ├── usuario_service.py          # Validações das regras de negócio para usuários
│   │   └── avaliacao_service.py        # Validações das regras de negócio para avaliações
|   |
│   ├── repositories/                   # Operações de acesso ao banco de dados
|   |   ├── empresa_repository.py       # Métodos para interagir com a tabela de empresas
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

**Descrição:**  :heavy_check_mark:

1. **models/:** Define as tabelas e entidades do banco de dados usando SQLAlchemy.

2. **routes/:** Define as rotas da API para cada entidade do sistema (projetos, usuários, avaliações).

3. **controllers/:** Implementam a lógica de controle, recebendo as requisições HTTP e invocando os serviços.

4. **services/:** Camada de lógica de negócio, aplica as restrições e lógicas mais específicas da aplicação,
 e processamento e integrações com serviços externos (IA, Firebase).

1. **validators/:**  Valida os dados de entrada antes de eles serem processados atraves das bibliotecas marshmallow e validate-docbr. Essa camada é responsável por checar formatos, tipos, e outras restrições básicas, garantindo que os dados estejam no formato correto antes de chegarem aos serviços ou controladores.

2. **repositories/:** Responsável por interagir com o banco de dados através do ORM SQLAlchemy.

3. **middleware/:** Implementa segurança e autenticação.

4. **utils/:** Funções auxiliares, como criptografia e gerenciamento de tokens.

5. **config/:** Configurações gerais da aplicação.

6.  **migrations/:** Contém as migrações de banco de dados, responsáveis por criar, alterar e manter as tabelas no PostgreSQL.

7.  **erros/:** Tratamento de exceções específicas e definição de classes de erro personalizadas para situações comuns ou críticas na aplicação.

8.  **requirements.txt:** Lista de todas as dependências e bibliotecas necessárias para o projeto (ex.: Flask, SQLAlchemy, Firebase SDK).

9.  **.env:** Arquivo de variáveis de ambiente sensíveis, como chaves de API, credenciais do Firebase, configurações de JWT, entre outros.

10. **app.py:** Arquivo principal que inicializa e executa a aplicação Flask.

11. **README.md:** Documentação do projeto, instruções de configuração, execução e detalhes de cada parte do sistema.

---

## Rotas - EndPoints :arrows_clockwise:

**1. Autenticação e Tokens** 🔑

**1.1. Login de usuário**
  - **Rota:** ```POST /users/login```
  - **Descrição:** Autentica um usuário e retorna um token JWT.
  - **Permissão:** Aberta (Não requer autenticação)
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**
    
    ```
    JSON
        {
            "email": "joao@email.com",
            "senha": "Senha123!"
        }
    ```    

  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**
  
    ```
    JSON
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "tipo": "avaliador"
        }
    ```    

...

**2. Usuários:** Gerenciamento de usuários cadastrados :bust_in_silhouette:

**2.1. Listar todos os usuários**
  - **Rota:** ```GET /users```
  - **Descrição:** Retorna todos os usuários cadastrados.
  - **Permissão:** Administradores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome": "joão silva",
                "email": "joao@email.com",
                "tipo": "avaliador",
                "data_cadastro": "2024-11-24T10:00:00Z"
            },
            {
                "id": "456e7890-a123-45d6-c789-426614174001",
                "nome": "maria oliveira",
                "email": "maria@email.com",
                "tipo": "administrador",
                "data_cadastro": "2024-11-23T09:30:00Z"
            }
        ]
    ```

...

**2.2. Obter um usuário por ID**
  - **Rota:** ```GET /users/{id}```
  - **Descrição:** Retorna informações de um usuário específico.
  - **Permissão:** Administradores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**
  
    ```
    JSON
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "nome": "joão silva",
            "email": "joao@email.com",
            "tipo": "avaliador",
            "data_cadastro": "2024-11-24T10:00:00Z"
        }
    ```

...

**2.3. Criar um novo usuário**
  - **Rota:** ```POST /users```
  - **Descrição:** Cadastra um novo usuário.
  - **Permissão:** Aberta (Não requer autenticação).
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**
      
        ```
        JSON
            {
                "nome": "João Silva",
                "email": "joao@email.com",
                "senha": "Senha123!",
                "tipo": "avaliador"
            }
        ```

  - **Resposta:**
    - **Status:** ```201 Created```
    - **Body:**

        ```
        JSON
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome": "joão silva",
                "email": "joao@email.com",
                "tipo": "avaliador",
                "data_cadastro": "2024-11-24T10:00:00Z"
            }
        ```      

...

**2.4. Atualizar um usuário**
  - **Rota:** ```PUT /users/{id}```
  - **Descrição:** Atualiza os dados de um usuário pelo ID.
  - **Permissão:** Administradores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**
  
        ```
        JSON
            {
                "nome": "João Oliveira",
                "email": "joao.oliveira@email.com",
                "tipo": "administrador"
            }
        ```

  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

        ```
        JSON
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome": "joão oliveira",
                "email": "joao.oliveira@email.com",
                "tipo": "administrador",
                "data_cadastro": "2024-11-24T10:00:00Z"
            }
        ```

...

**2.5. Deletar um usuário**
  - **Rota:** ```DELETE /users/{id}```
  - **Descrição:** Remove um usuário pelo ID.
  - **Permissão:** Administradores autenticados.
  - **Descrição:** Remove um usuário pelo ID.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```204 No Content```

...

**3. Empresas:** Gerenciamento de empresas cadastradas :office:

**3.1. Listar todas as empresas**
  - **Rota:** ```GET /companies```
  - **Descrição:** Retorna todas as empresas cadastradas.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**
  
    ```
    JSON

        [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome_fantasia": "Empresa X",
                "cnpj": "12345678000100",
                "email": "contato@empresa.com",
                "data_cadastro": "2024-11-24T10:00:00Z"
            },
            {
                "id": "456e7890-a123-45d6-c789-426614174001",
                "nome_fantasia": "Empresa Y",
                "cnpj": "98765432000199",
                "email": "contato@empresay.com",
                "data_cadastro": "2024-11-23T09:30:00Z"
            }
        ]
    ```  

...

**3.2. Obter uma empresa por ID**
  - **Rota:** ```GET /companies/{id}```
  - **Descrição:** Retorna informações de uma empresa específica.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "nome_fantasia": "Empresa X",
        "cnpj": "12345678000100",
        "email": "contato@empresa.com",
        "data_cadastro": "2024-11-24T10:00:00Z"
    }
    ```

...

**3.2. Criar uma nova empresa**
  - **Rota:** ```POST /companies```
  - **Descrição:** Cadastra uma nova empresa.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**

    ```
    JSON
        {
            "nome_fantasia": "Empresa X",
            "cnpj": "12345678000100",
            "email": "contato@empresa.com"
        }
    ```    

  - **Resposta:**
    - **Status:** ```201 Created```
    - **Body:**

    ```
    JSON
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "nome_fantasia": "Empresa X",
            "cnpj": "12345678000100",
            "email": "contato@empresa.com",
            "data_cadastro": "2024-11-24T10:00:00Z"
        }
    ```  

...

**3.3. Atualizar uma empresa**
  - **Rota:** ```PUT /companies/{id}```
  - **Descrição:** Atualiza os dados de uma empresa pelo ID.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**

    ```
    JSON

        {
            "nome_fantasia": "Empresa Atualizada",
            "cnpj": "12345678000100",
            "email": "contato@empresaatualizada.com"
        }
    ```

  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "nome_fantasia": "Empresa Atualizada",
            "cnpj": "12345678000100",
            "email": "contato@empresaatualizada.com",
            "data_cadastro": "2024-11-24T10:00:00Z"
        }
     ```    

...

**3.4. Deletar uma empresa**
  - **Rota:** DELETE /companies/{id}
  - **Descrição:** Remove uma empresa pelo ID.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```204 No Content```

...

**4. Projetos:** Gerenciamento de projetos submetidos :page_facing_up:

**4.1. Listar todos os projetos**
  - **Rota:** ```GET /projects```
  - **Descrição:** Retorna todos os projetos cadastrados.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        [
            {
                "id": "789e1234-f89b-12d3-a456-426614174000",
                "titulo_projeto": "projeto softex",
                "status": "em avaliação",
                "arquivo": "https://firebase.com/projeto1.pdf",
                "data_submissao": "2024-11-24T11:00:00Z"
            } 
        ]
    ```    

...

**4.2. Criar um projeto**
  - **Rota:** ```POST /projects```
  - **Descrição:** Cria um novo projeto.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: multipart/form-data```
    - **Body:**

    ```
    JSON
        {
            "titulo_projeto": "Projeto Softex",
            "status": "em avaliação",
            "arquivo": "<arquivo_pdf>"
        }

    ```        

  - **Resposta:**
    - **Status:** ```201 Created```
    - **Body:**

    ```
    JSON
        {
            "id": "789e1234-f89b-12d3-a456-426614174000",
            "titulo_projeto": "projeto softex",
            "status": "em avaliação",
            "arquivo": "https://firebase.com/projeto1.pdf",
            "data_submissao": "2024-11-24T11:00:00Z"
        }
    ```    

...

**4.4. Atualizar um projeto**
  - **Rota:** ```PUT /projects/{id}```
  - **Descrição:** Atualiza os dados de um projeto pelo ID.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**

    ```
    JSON
        {
            "titulo_projeto": "Projeto Softex Atualizado",
            "status": "aprovado"
        }
    ```    

  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        {
            "id": "789e1234-f89b-12d3-a456-426614174000",
            "titulo_projeto": "projeto softex atualizado",
            "status": "aprovado",
            "arquivo": "https://firebase.com/projeto1.pdf",
            "data_submissao": "2024-11-24T11:00:00Z"
        }
    ```    

...

**4.5. Atualizar o status de um projeto**
  - **Rota:** ```PATCH /projects/{id}/status```
  - **Descrição:** Atualiza o status de um projeto.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**

    ```
    JSON
        {
            "status": "aprovado"
        }
    ```    

  - **Resposta:**
  - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        {
            "id": "789e1234-f89b-12d3-a456-426614174000",
            "titulo_projeto": "projeto softex",
            "status": "aprovado",
            "arquivo": "https://firebase.com/projeto1.pdf",
            "data_submissao": "2024-11-24T11:00:00Z"
        }
    ```    

...

**4.6. Deletar um projeto**
  - **Rota:** ```DELETE /projects/{id}```
  - **Descrição:** Remove um projeto pelo ID.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```204 No Content```

...

**5. Avaliações:** Gerenciamento de avaliações dos projetos :star:

**5.1. Listar todas as avaliações**
  - **Rota:** ```GET /reviews```
  - **Descrição:** Retorna todas as avaliações cadastradas.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        [
            {
                "id": "123e4567-f89b-12d3-a456-426614174000",
                "projeto_id": "789e1234-f89b-12d3-a456-426614174000",
                "feedback_qualitativo": "Ótimo trabalho!",
                "data_avaliacao": "2024-11-24T11:00:00Z"
            }
        ]
    ```    

...

**5.2. Obter uma avaliação por ID**
  - **Rota:** ```GET /reviews/{id}```
  - **Descrição:** Retorna informações de uma avaliação específica.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        {
            "id": "123e4567-f89b-12d3-a456-426614174000",
            "projeto_id": "789e1234-f89b-12d3-a456-426614174000",
            "feedback_qualitativo": "Ótimo trabalho!",
            "data_avaliacao": "2024-11-24T11:00:00Z"
        }
    ```    

...

**5.3. Criar uma nova avaliação utilizando IA**
  - **Rota:** ```POST /reviews```
  - **Descrição:** Cria uma nova avaliação automaticamente utilizando inteligência artificial, API OpenAI (ChatGPT), e critérios padronizados com base na Lei do Bem.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**

    ```
    JSON
        {
            "projeto_id": "789e1234-f89b-12d3-a456-426614174000"
        }
    ```

  - **Resposta:**
    - **Status:** ```201 Created```
    - **Body:**

    ```
    JSON
        {
            "id": "123e4567-f89b-12d3-a456-426614174000",
            "projeto_id": "789e1234-f89b-12d3-a456-426614174000",
            "feedback_qualitativo": "O projeto apresenta um alto grau de inovação e alinhamento com os critérios da Lei do Bem.",
            "data_avaliacao": "2024-11-24T11:00:00Z"
        }
    ```    
<br>

> [!Note]\
> A rota `POST /reviews` utiliza a API OpenAI (ChatGPT) para análise automática, aplicando critérios pré-definidos com base na Lei do Bem, fornecendo um feedback inicial de alta qualidade e eficiência.
<br>

...

**5.4. Atualizar uma avaliação manualmente**
  - **Rota:** ```PUT /reviews/{id}```
  - **Descrição:** Permite ao avaliador atualizar manualmente uma avaliação previamente realizada. Atualiza os dados de uma avaliação pelo ID.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Requisição:**
    - **Headers:** ```Content-Type: application/json```
    - **Body:**

    ```
    JSON
        {
            "feedback_qualitativo": "O projeto apresenta um alto grau de inovação e alinhamento com os critérios da Lei do Bem. 
            Apresenta oportunidades de melhoria em viabilidade técnica."
        }
    ```    

  - **Resposta:**
    - **Status:** ```200 OK```
    - **Body:**

    ```
    JSON
        {
            "id": "123e4567-f89b-12d3-a456-426614174000",
            "projeto_id": "789e1234-f89b-12d3-a456-426614174000",
            "feedback_qualitativo": "O projeto apresenta um alto grau de inovação e alinhamento com os critérios da Lei do Bem. 
            Apresenta oportunidades de melhoria em viabilidade técnica.",
            "data_avaliacao": "2024-11-24T11:00:00Z"
        }
    ```    
<br>

> [!Note]\
> A rota `PUT /reviews/{id}` é destinada a ajustes manuais feitos pelo avaliador, garantindo flexibilidade para refinamentos adicionais e observações específicas.
<br>
    
...

**5.5. Deletar uma avaliação**
  - **Rota:** ```DELETE /reviews/{id}```
  - **Descrição:** Remove uma avaliação pelo ID.
  - **Permissão:** Avaliadores autenticados.
  - **Cabeçalho de Autenticação:** ```Authorization: Bearer <token>```
  - **Resposta:**
    - **Status:** ```204 No Content```

...

**Observações:**
  - **Cabeçalho de Autenticação:** Para rotas protegidas, inclua:

    ``` 
    Authorization: Bearer <token>
    ``` 

  - **Permissões:**
    - **Aberta:** Não requer autenticação.
    - **Avaliadores autenticados:** Requer um token JWT válido com permissões para avaliadores, usuários do tipo avaliador.
    - **Administradores autenticados:** Requer um token JWT válido com permissões administrativas, usuários do tipo administrador.

---

## Clonar Repositório :file_folder: :arrow_right: :file_folder:

```bash
git clone https://github.com/chat-softex/backend.git
```

---

## Contribuições :technologist:

**Contribuições são bem-vindas! Se você deseja contribuir com melhorias ou correções para o projeto, basta seguir estes passos:**

- Faça um fork do projeto.
- Crie uma branch para sua nova funcionalidade (git checkout -b feat/nova-funcionalidade).
- Faça commit das suas alterações (git commit -m 'Adiciona nova funcionalidade').
- Envie para o repositório remoto (git push origin feat/nova-funcionalidade).
- Crie um pull request.

---

## Configuração e Instalação :gear:

### Criar e ativar ambiente virtual :white_check_mark:

**Criar ambiente virtual:**
```bash
python -m venv venv
```

**Ativar ambiente virtual - MacOS/Linux:**
```bash
source venv/bin/activate
```

**Ativar ambiente virtual - Windows:**
```bash
venv\Scripts\activate 
```

---

### Configurar as variáveis de ambiente :white_check_mark:
- Altere o arquivo "example.env" para ".env".
- Preencha as informações relacionadas ao HOTS, PORT, DATABASE, PASSWORD e USERNAME do SGBD.
- Preencha as informações relacionadas ao nome do BUCKET do Firebase e ao PATH do arquivo JSON contendo as configurações do Firebase.
- Preencha as informações relacionadas as chaves secretas do SECRET_KEY, JWT_SECRET_KEY, ENCRYPTION_KEY e OPENAI_KEY.

---

### Instalação das depedências :arrow_down_small:

```bash
pip install -r requirements.txt

```

---

### Iniciação e migration Database :file_folder:

**Inicializar o ambiente de Migration:**
```bash
flask db init

```

**Criar Migration:**
```bash
flask db migrate -m "Initial migration"

```

**Aplicar Migration ao banco de dados:**
```bash
flask db upgrade

```

---

### Executar app :arrow_forward:

**development:**
```bash
flask run

```

```bash
Running on http://127.0.0.1:5000/

```

---  

## Licença 

The [MIT License]() (MIT)

Copyright :copyright: 2024 - ChatSoftex
