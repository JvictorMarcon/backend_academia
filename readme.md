# 🏋️‍♂️ API GYM - Sistema de Gerenciamento de Academia

> **Projeto Acadêmico - SENAI** > Este projeto foi desenvolvido como parte do currículo do SENAI, com o objetivo de aplicar conceitos de arquitetura de software onde o **Backend** e o **Frontend** operam de forma totalmente separada (desacoplada). 

Esta API REST foi construída em **Python** com **Flask** para gerenciar o cadastro de alunos, utilizando o **Firebase Firestore** para persistência de dados em nuvem e **JWT** para segurança.

---

## 🔗 Links do Projeto

### 💻 Frontend
* **Deploy (Vercel):** [https://seuprompt-front.vercel.app](INSIRA_O_LINK_AQUI)
* **Repositório:** [https://github.com/seu-usuario/projeto-gym-frontend](INSIRA_O_LINK_AQUI)
* **Clonar:** `git clone https://github.com/seu-usuario/projeto-gym-frontend.git`

### ⚙️ Backend (Esta API)
* **Deploy (Vercel):** [https://backendacademia.vercel.app/](INSIRA_O_LINK_AQUI)
* **Repositório:** [https://github.com/JvictorMarcon/backend_academia.git](INSIRA_O_LINK_AQUI)
* **Clonar:** `git clone https://github.com/JvictorMarcon/backend_academia.git`

---

## 🚀 Funcionalidades

* **Arquitetura Desacoplada**: Backend independente que serve dados via JSON para o Frontend.
* **Autenticação Administrativa**: Login seguro com geração de Token JWT.
* **Gerenciamento de Clientes (CRUD)**: 
    * Listagem completa de alunos.
    * Busca individual por CPF.
    * Cadastro de novos alunos com ID incremental.
    * Atualização parcial (PATCH) de dados e status.
    * Exclusão definitiva de registros.
* **Tratamento de Erros**: Respostas padronizadas para erros 404 e 500.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework:** Flask
* **Banco de Dados:** Google Firebase Firestore
* **Segurança:** Flask-CORS e PyJWT
* **Documentação:** OpenAPI 3.0 (Swagger)

---

## 📋 Documentação das Rotas

### 🔓 Rotas Públicas
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Status da API e Autores. |
| `GET` | `/clientes` | Retorna todos os alunos cadastrados. |
| `GET` | `/clientes/<int:cpf>` | Busca um aluno específico pelo CPF. |
| `POST` | `/login` | Autentica o ADM e gera o Token de acesso. |

### 🔐 Rotas Privadas (Requer Token no Header)
*Header: `Authorization: Bearer <seu_token>`*

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/clientes` | Cadastra um novo aluno. |
| `PATCH` | `/clientes/<int:cpf>` | Edita informações (nome, cpf ou status). |
| `DELETE` | `/clientes/<int:cpf>` | Remove um aluno do banco de dados. |

---

## 📖 Como testar com Swagger

1. Copie o código do arquivo `openapi.yaml` (presente na raiz deste projeto).
2. Acesse o [Swagger Editor](https://editor.swagger.io/).
3. Cole o código para visualizar a documentação interativa e os exemplos de JSON para cada requisição.

---

## ⚙️ Configuração Local

1.  **Instale as dependências:**
    ```bash
    pip install flask flask-cors firebase-admin python-dotenv flasgger pyjwt
    ```
2.  **Variáveis de Ambiente (.env):**
    Crie um arquivo `.env` e configure:
    ```env
    SECRET_KEY=sua_chave_segura
    ADM_USUARIO=seu_usuario
    ADM_SENHA=sua_senha
    # Se estiver usando Vercel, adicione a FIREBASE_KEY em JSON
    ```
3.  **Firebase:**
    Certifique-se de ter o arquivo `firebase.json` na raiz para autenticação com o SDK do Google.

4.  **Execução:**
    ```bash
    python app.py
    ```

---

## 👥 Autores
* **João Victor**
* **Guilherme**

--
*Este projeto é para fins educacionais - SENAI 2026.*