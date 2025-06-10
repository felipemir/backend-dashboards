API - Galeria de Dashboards

API de backend desenvolvida em Python com FastAPI para gerenciar o acesso a uma galeria de dashboards de Business Intelligence. O objetivo principal do backend é gerenciar usuários, controlar o acesso por meio de autenticação e fornecer os dados dos dashboards de acordo com as permissões de cada usuário.

✨ Features Principais

    Autenticação de Usuários: Sistema de login seguro utilizando username e password para gerar tokens de acesso.

Autorização baseada em Roles: O sistema suporta dois níveis de permissão:

    secretaria: Acesso irrestrito a todos os dashboards.

gestor: Acesso restrito aos dashboards que pertencem exclusivamente ao seu setor.

Tokens JWT: A comunicação com os endpoints protegidos é stateless e utiliza JSON Web Tokens (JWT) para garantir a segurança.
Armazenamento Seguro de Senhas: As senhas são hasheadas com o algoritmo bcrypt antes de serem salvas no banco de dados, nunca sendo armazenadas em texto plano.
Serviço Dinâmico de Dados: Substitui os dados estáticos que existiam no frontend por uma fonte de dados dinâmica e segura, vinda do banco de dados.

🛠️ Tecnologias Utilizadas

    Backend: Python 3.12
    Framework: FastAPI
    Banco de Dados: MySQL
    ORM: SQLAlchemy
    Validação de Dados: Pydantic
    Autenticação: Passlib (para hashing), Python-JOSE (para JWT)
    Servidor ASGI: Uvicorn

📂 Estrutura do Projeto

/galeria-backend
├── .env                # Arquivo com as variáveis de ambiente (segredos)
├── main.py             # Arquivo principal da aplicação FastAPI, define os endpoints
├── auth.py             # Funções de segurança (hashing de senha, criação/validação de token JWT)
├── crud.py             # Funções que interagem com o banco de dados (Create, Read, Update, Delete)
├── database.py         # Configuração da conexão com o banco de dados (SQLAlchemy)
├── models.py           # Modelos de dados do SQLAlchemy (representação das tabelas do banco)
├── schemas.py          # Esquemas do Pydantic (validação da estrutura dos dados da API)
└── requirements.txt    # Lista de dependências Python do projeto

🗃️ Banco de Dados

O backend utiliza um banco de dados MySQL para persistir as informações. O modelo de dados é dividido em duas tabelas principais: users e dashboards.
Tabela users

Armazena as informações dos usuários que podem acessar o sistema.

    id: Identificador único.
    username: Nome de usuário para login.

password: Hash da senha do usuário.
role: Nível de permissão, pode ser 'secretaria' ou 'gestor'.
sector: Setor do usuário, obrigatório se a role for 'gestor'.

Tabela dashboards

Armazena os metadados dos dashboards que serão exibidos na galeria.

    id: Identificador único.
    title, type, description: Informações descritivas do dashboard.

sector: Setor responsável pelo dashboard. Este campo é a chave para a regra de permissão.

    url: O link direto para o dashboard (ex: Power BI).

Como Tudo se Relaciona

O sistema de permissão funciona conectando as duas tabelas. Quando um usuário do tipo gestor faz uma requisição para ver os dashboards, o fluxo é o seguinte:

    O token JWT do usuário é decodificado para extrair seu sector (ex: 'GTI').

O backend faz uma consulta na tabela dashboards.
A consulta é filtrada para retornar apenas os registros onde a coluna sector da tabela dashboards seja igual ao sector do usuário.
Dessa forma, um gestor da 'GTI' só recebe a lista de dashboards que também pertencem à 'GTI'. O usuário secretaria ignora essa regra e tem acesso a todos os registros.

🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento local.
Pré-requisitos

    Python 3.10+
    Servidor MySQL em execução

1. Configuração do Banco de Dados

Conecte-se ao seu MySQL e execute os seguintes comandos para criar o banco, as tabelas e inserir dados de teste:
SQL

CREATE DATABASE galeria_db;
USE galeria_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('secretaria', 'gestor') NOT NULL,
    sector VARCHAR(255),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE dashboards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type ENUM('BI', 'REPORT') NOT NULL,
    description TEXT,
    updatedDate VARCHAR(10) NOT NULL,
    tags JSON NOT NULL,
    sector VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL
);

-- Inserir usuários de teste (senha para todos é: senha123)
INSERT INTO users (username, password, role, sector) VALUES 
('secretaria', '$2b$12$Ea.r9UU74dD6s1gA8A93y.o8emg17Dgrw10pDDq2m88VsGGS1IZLi', 'secretaria', NULL),
('gestor.gti', '$2b$12$Ea.r9UU74dD6s1gA8A93y.o8emg17Dgrw10pDDq2m88VsGGS1IZLi', 'gestor', 'GTI');

2. Configuração do Ambiente

Clone o repositório e navegue até a pasta do projeto.

Crie e ative um ambiente virtual:
Bash

# Criar o ambiente
python3 -m venv venv

# Ativar (Linux/macOS com Fish)
source venv/bin/activate.fish

# Ativar (Linux/macOS com Bash)
# source venv/bin/activate

Instale as dependências:
(Primeiro, crie o arquivo requirements.txt com o comando pip freeze > requirements.txt no seu terminal, depois:)
Bash

pip install -r requirements.txt

Configure as variáveis de ambiente:
Crie um arquivo chamado .env na raiz do projeto e copie o conteúdo abaixo, ajustando com suas credenciais.
Snippet de código

DATABASE_URL="mysql+mysqlclient://<SEU_USUARIO>:<SUA_SENHA>@<HOST_DO_BANCO>/galeria_db"
JWT_SECRET_KEY="coloque-uma-chave-secreta-muito-forte-aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

3. Rode a Aplicação

Com o ambiente virtual ativo, execute o seguinte comando:
Bash

uvicorn main:app --reload

A API estará disponível em http://127.0.0.1:8000. A documentação interativa para testes estará em http://127.0.0.1:8000/docs.
📈 Melhorias Futuras

Conforme o documento de requisitos, os próximos passos para este projeto incluem:

    CRUD de Dashboards: Endpoints para criar, atualizar e deletar dashboards, acessíveis apenas pelo perfil secretaria.

CRUD de Usuários: Endpoints para gerenciar usuários, também protegidos e restritos ao perfil secretaria.