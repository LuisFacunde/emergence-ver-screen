# Sistema de Pesquisa de Pacientes

Sistema completo de pesquisa de pacientes com frontend React e backend Flask.

## Estrutura do Projeto

```
emergence-ver-screen/
├── backend/                 # Backend Flask
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/               # Frontend React
    └── emergence-ver/
        ├── src/
        │   ├── services/
        │   │   └── api.js
        │   ├── App.jsx
        │   ├── App.css
        │   └── index.css
        └── package.json
```

## Executar o Projeto

### Backend (Flask)

```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```

Servidor disponível em: http://localhost:5000

### Frontend (React)

```bash
cd frontend/emergence-ver
npm install
npm run dev
```

Aplicação disponível em: http://localhost:5174

## Documentação

- [Backend README](backend/README.md) - Documentação completa do backend Flask
- Frontend - Interface de pesquisa de pacientes com dados mockados

## Funcionalidades

### Backend
- ✅ API RESTful completa
- ✅ Endpoints para Users e Items
- ✅ CORS configurado
- ✅ Validação de dados
- ✅ Tratamento de erros

### Frontend
- ✅ Interface de pesquisa por Prontuário e Nome
- ✅ Tabela de resultados com paginação
- ✅ Design responsivo
- ✅ Dados mockados
- ✅ Preparado para integração com backend

## Integração

O frontend está preparado para integração com o backend. Para conectar:

1. Descomente as funções da API em `frontend/emergence-ver/src/services/api.js`
2. Atualize `App.jsx` para usar as funções da API real
3. Configure os endpoints no backend para pacientes

## Licença

Este projeto é parte do Emergence Ver Screen.
