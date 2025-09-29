# Controle de Gastos - API

API desenvolvida para gerenciamento de categorias e gastos pessoais, utilizando Flask, SQLAlchemy e OpenAPI3.

---

## 📚 Sobre o Projeto
Projeto acadêmico da disciplina de Desenvolvimento Full Stack (Pós-graduação em Engenharia de Software - PUC Rio).

## 🚀 Funcionalidades
- CRUD completo de **categorias** e **gastos**.
- Relacionamento entre gastos e categorias.
- Documentação interativa via Swagger, Redoc e RapiDoc.

## 🛠️ Instalação

### 1. Pré-requisitos
- Python 3.13+
- Git (opcional)

### 2. Clonando o projeto
```bash
git clone <url-do-repositorio>
```

### 3. Ambiente virtual
```bash
cd mvp/meu_app_api
python -m venv ../env
```

### 4. Ativando o ambiente virtual
- **Windows (PowerShell):** `../env/Scripts/Activate.ps1`
- **Windows (cmd):** `../env/Scripts/activate.bat`
- **Linux/Mac:** `source ../env/bin/activate`

### 5. Instalando dependências
```bash
pip install -r requirements.txt
```

### 6. Executando a API
```bash
flask run --host 0.0.0.0 --port 5000
```

---

## 📑 Endpoints

### Categorias
| Método | Rota                        | Descrição                  |
|--------|-----------------------------|----------------------------|
| POST   | `/categorias`               | Adiciona uma categoria     |
| GET    | `/categorias`               | Lista todas as categorias  |
| GET    | `/categorias/<uuid:id>`     | Busca categoria por ID     |
| PUT    | `/categorias/<uuid:id>`     | Atualiza categoria         |
| PATCH  | `/categorias/<uuid:id>`     | Atualiza parcialmente      |
| DELETE | `/categoria/<uuid:id>`      | Remove categoria           |

### Gastos
| Método | Rota                        | Descrição                  |
|--------|-----------------------------|----------------------------|
| POST   | `/gastos`                   | Adiciona um gasto          |
| GET    | `/gastos`                   | Lista todos os gastos      |
| GET    | `/gastos/<uuid:id>`         | Busca gasto por ID         |
| PUT    | `/gastos/<uuid:id>`         | Atualiza gasto             |
| PATCH  | `/gastos/<uuid:id>`         | Atualiza parcialmente      |
| DELETE | `/gasto/<uuid:id>`          | Remove gasto               |

---

## 📄 Documentação Interativa
Acesse [`/openapi`](http://localhost:5000/openapi) para visualizar a documentação via Swagger, Redoc ou RapiDoc.

## ⚡ Observações
- Os dados são armazenados em SQLite (`database/db.sqlite3`).
- O banco é criado automaticamente ao iniciar o app.
- O projeto utiliza Pydantic para validação dos dados.
- Para dúvidas, consulte os arquivos de schema e model.

---

## 👤 Autor

| Nome                          | LinkedIn                                                                 | GitHub                                      |
|-------------------------------|--------------------------------------------------------------------------|---------------------------------------------|
| Fabricio dos Santos da Silva   | [linkedin.com/in/fabriciossilva](https://www.linkedin.com/in/fabriciossilva/) | [github.com/FabriciodSantosSilva](https://github.com/FabriciodSantosSilva) |

