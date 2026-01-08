# Backend Flask - Emergence Ver Screen

Backend em Python com Flask para o projeto Emergence Ver Screen.

## 📋 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste conforme necessário:

```bash
copy .env.example .env
```

## ▶️ Executar o servidor

```bash
python app.py
```

O servidor estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
backend/
├── api/                    # Módulo da API
│   ├── __init__.py        # Inicialização do blueprint
│   ├── routes.py          # Rotas da API
│   └── models.py          # Modelos de dados
├── utils/                 # Utilitários
│   ├── __init__.py
│   └── helpers.py         # Funções auxiliares
├── app.py                 # Aplicação principal
├── config.py              # Configurações
├── requirements.txt       # Dependências
├── .env.example          # Template de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Documentação
```

## 🔌 API Endpoints

### Health Check
- **GET** `/api/health` - Verifica se a API está funcionando

### Usuários
- **GET** `/api/users` - Lista todos os usuários
- **GET** `/api/users/:id` - Busca um usuário específico
- **POST** `/api/users` - Cria um novo usuário
- **PUT** `/api/users/:id` - Atualiza um usuário
- **DELETE** `/api/users/:id` - Remove um usuário

### Itens
- **GET** `/api/items` - Lista todos os itens
- **GET** `/api/items/:id` - Busca um item específico
- **POST** `/api/items` - Cria um novo item
- **PUT** `/api/items/:id` - Atualiza um item
- **DELETE** `/api/items/:id` - Remove um item

## 📝 Exemplos de Uso

### Criar um usuário

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "João Silva", "email": "joao@example.com"}'
```

### Listar todos os itens

```bash
curl http://localhost:5000/api/items
```

### Atualizar um item

```bash
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Novo Título", "description": "Nova descrição"}'
```

## 🔧 Configuração

As configurações podem ser ajustadas no arquivo `.env`:

- `FLASK_ENV` - Ambiente (development, production, testing)
- `FLASK_DEBUG` - Modo debug (True/False)
- `PORT` - Porta do servidor (padrão: 5000)
- `CORS_ORIGINS` - Origens permitidas para CORS (separadas por vírgula)

## 🌐 CORS

O CORS está configurado para aceitar requisições do frontend React. Por padrão, as origens permitidas são:
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (Create React App)

Para adicionar mais origens, edite a variável `CORS_ORIGINS` no arquivo `.env`.

## 📦 Dependências

- **Flask** - Framework web
- **Flask-CORS** - Suporte a CORS
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Werkzeug** - Utilitários WSGI

## 🔄 Formato de Resposta

Todas as respostas da API seguem um formato padronizado:

### Sucesso
```json
{
  "success": true,
  "data": { ... }
}
```

### Erro
```json
{
  "success": false,
  "error": {
    "message": "Mensagem de erro",
    "code": 400
  }
}
```

## 🚧 Desenvolvimento

Este é um backend de exemplo com dados em memória. Para produção, considere:

- Adicionar um banco de dados (PostgreSQL, MySQL, MongoDB)
- Implementar autenticação e autorização (JWT)
- Adicionar validação de dados mais robusta
- Implementar testes automatizados
- Configurar logging adequado
- Adicionar rate limiting
- Implementar cache

## 📄 Licença

Este projeto é parte do Emergence Ver Screen.
