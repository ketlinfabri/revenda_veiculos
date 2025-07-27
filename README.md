
# 🚗 API de Revenda de Veículos

API REST desenvolvida com **FastAPI** para gerenciar um sistema de revenda de veículos com autenticação via **AWS Cognito**.

---

## 🧰 Tecnologias utilizadas

- **FastAPI** – framework web moderno e rápido
- **SQLAlchemy** – ORM para interagir com banco PostgreSQL
- **Pydantic** – validação de dados
- **AWS Cognito** – autenticação de usuários
- **Docker** - execar as aplicações

---

## 🚀 Como executar

#### Subir os serviços (API + Banco de Dados)

Para instalar as dependências necessárias, execute o seguinte comando apontando para o arquivo requirements.txt:
```bash
pip install -r requirements.txt
````
Após, execute o comando no terminal:
```bash
docker-compose up --build
````

Acesse a API em: http://localhost:8000/docs
Acesse o BD Postgres em http://localhost:5432. Sugestâo: executar pela PGAdmin, com as credenciais:
  * Para fins de teste, deixei dois veículos que serâo cadastrados na inicialização do banco.

É necessário que o serviço de Auth tenha sido previamente subido e executado em http://localhost:8080/docs para cadastro e obtentação do token do usário.

---

## 📑 Documentação da API

- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Autenticação AWS Cognito

O token para realizar a compra do veículo deve ser obtido através da API de Auth - serviço apartado para cadastro e login de usuário no Cognito (AWS).

```
Authorization: Bearer <token_cognito>
```

---

## 📌 Endpoints principais

### 🔍 Cadastrar veículo

`POST /veiculos`

### 🔍 Listar veículos vendidos

`GET /veiculos/vendidos`

### 🔍 Listar veículos disponíveis

`GET /veiculos/disponiveis`

### 💰 Comprar veículo

`POST /comprar/{id_veiculo}`
- Requer autenticação do usuário através de um token válido do Cognito

---

## ‍💻 Repositório
   https://github.com/ketlinfabri/revenda_veiculos

## ‍💻 Desenvolvido por

Ketlin Fabri dos Santos  - rm354534 | Trabalho Fase 3
