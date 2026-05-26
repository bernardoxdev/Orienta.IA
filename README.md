# Orienta.IA

Sistema inteligente de apoio à orientação acadêmica para projetos de:

- Iniciação Científica (IC)
- Trabalho de Conclusão de Curso (TCC)
- Mestrado
- Doutorado

O projeto tem como objetivo auxiliar orientadores e orientandos através de uma plataforma integrada com:

- Gerenciamento de tarefas
- Acompanhamento de progresso
- Autenticação segura
- Integração com Telegram
- Automação de processos acadêmicos
- Suporte futuro por Inteligência Artificial

---

# Objetivos

O Orienta.IA busca melhorar o acompanhamento acadêmico através de ferramentas digitais modernas, permitindo:

- comunicação centralizada
- acompanhamento contínuo do orientando
- registro de progresso
- organização documental
- automação de notificações
- análise inteligente de desempenho acadêmico

---

# Funcionalidades Atuais

- API REST com FastAPI
- Integração com Telegram utilizando Pyrogram
- Sistema de autenticação JWT
- Controle de permissões por roles
- Banco de dados PostgreSQL
- Docker e Docker Compose
- Sistema modularizado
- Estrutura preparada para integração com IA

---

# Tecnologias Utilizadas

## Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pyrogram
- PostgreSQL
- Passlib
- Argon2
- JWT
- Uvicorn

## Infraestrutura

- Docker
- Docker Compose

## Frontend

- HTML
- CSS
- JavaScript

---

# Arquitetura do Projeto

```text
backend/
├── core/          # Configurações centrais
├── database/      # Banco de dados e modelos
├── events/        # Eventos globais
├── ia/            # Módulos de IA
├── messages/      # Handlers do bot Telegram
├── routes/        # Rotas da API
├── services/      # Regras de negócio
└── utils/         # Utilitários do sistema
```

---

# Estrutura dos Componentes

## api.py

Responsável por inicializar a API FastAPI.

## bot.py

Responsável pela inicialização do bot Telegram.

## backend/core

Contém:

- autenticação JWT
- segurança
- rate limiting
- configurações globais

## backend/database

Contém:

- conexão com banco
- modelos SQLAlchemy
- schemas
- inicialização do banco

## backend/messages

Sistema de handlers do Telegram.

## backend/routes

Rotas HTTP da API.

## backend/services

Camada de regras de negócio.

## backend/utils

Funções auxiliares reutilizáveis.

---

# Sistema de Roles

O sistema possui suporte para múltiplos níveis de permissão:

- user
- aluno
- professor
- orientador
- administrador

---

# Segurança

O projeto utiliza:

- autenticação JWT
- hash de senhas com Argon2
- rate limiting
- separação de permissões
- variáveis de ambiente

---

# Instalação

## Clonando o repositório

```bash
git clone https://github.com/bernardoxdev/Orienta.IA
cd Orienta.IA
```

---

# Configuração de ambiente

Crie um arquivo `.env`:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

TELEGRAM_API_ID=
TELEGRAM_API_HASH=
TELEGRAM_BOT_TOKEN=

JWT_SECRET_KEY=
```

---

# Executando com Docker

```bash
docker compose up -d --build
```

---

# Executando manualmente

## Instalar dependências

```bash
pip install .
```

## Rodar API

```bash
python api.py
```

## Rodar Bot

```bash
python bot.py
```

## Rodar Site

```bash
python site.py
```

---

# Dependências do Projeto

```toml
[project]
name = "Orienta.IA"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "bcrypt>=5.0.0",
    "brutils>=2.4.0",
    "fastapi>=0.136.1",
    "httpx>=0.28.1",
    "limits>=5.8.0",
    "numpy>=2.4.4",
    "argon2-cffi>=25.1.0",
    "passlib>=1.7.4",
    "psycopg2-binary>=2.9.12",
    "pyrogram>=2.0.106",
    "python-dotenv>=1.2.2",
    "python-jose[cryptography]>=3.5.0",
    "slowapi>=0.1.9",
    "sqlalchemy>=2.0.49",
    "tgcrypto>=1.2.5",
    "uvicorn[standard]>=0.46.0",
]
```

---

# Roadmap Futuro

- Painel Web administrativo
- IA para acompanhamento acadêmico
- Geração automática de cronogramas
- Análise de produtividade
- Sistema de recomendações
- Integração com LLMs
- Geração de relatórios acadêmicos
- Dashboard em tempo real

---

# Licença

Este projeto está licenciado sob a licença CC0-1.0 license.

---

# Autor

Projeto desenvolvido por Bernardo Castro para pesquisa de Iniciação Científica.