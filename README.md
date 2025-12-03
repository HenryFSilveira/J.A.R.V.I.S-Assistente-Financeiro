# 💰 J.A.R.V.I.S: Assistente LLM Especializado em Finanças

## 🎯 Objetivo e Proposta do Projeto

O objetivo deste projeto é o **Desenvolvimento de um Microsserviço em Python** usando o framework **FastAPI**, que atua como um Assistente Inteligente especializado em **Finanças e Investimentos**. O assistente integra-se ao modelo **Google Gemini** para fornecer análises, dicas de orçamento e explicações sobre termos e estratégias financeiras.

### Funcionalidade Chave
A arquitetura implementa o **gerenciamento de contexto conversacional individual** por `user_id`, garantindo que a API mantenha o histórico de conversa de cada usuário isoladamente.

## 🛠️ Tecnologias Utilizadas

* **Backend Framework:** **FastAPI**
* **Modelo de IA:** Google **Gemini** (via biblioteca `google-genai`)
* **Gestão de Contexto:** Dicionário em memória indexado por `user_id`
* **Frontend (Interface Web):** **Streamlit**

---

## ⚙️ Como Utilizar o J.A.R.V.I.S

### 1. Instruções de Instalação e Setup

1.  **Clonar e Instalar Dependências:**
    ```bash
    # 1. Clonar o repositório
    git clone [https://github.com/HenryFSilveira/J.A.R.V.I.S-Assistente-Financeiro.git](https://github.com/HenryFSilveira/J.A.R.V.I.S-Assistente-Financeiro.git)
    cd J.A.R.V.I.S-Assistente-Financeiro

    # 2. Criar e ativar o ambiente virtual
    python -m venv venv
    .\venv\Scripts\Activate.ps1

    # 3. Instalar todas as dependências do projeto (via requirements.txt)
    pip install -r requirements.txt --only-binary :all:
    ```

2.  **Configuração da Chave de API:**
    Crie um arquivo chamado **`.env`** na raiz do projeto e insira sua chave de API.

    *Atenção: O `.gitignore` impede que este arquivo seja enviado ao repositório, mantendo sua chave segura.*

    ```env
    # .env
    GEMINI_API_KEY="SUA_CHAVE_DE_API_GEMINI_AQUI"
    ```

### 2. 🚀 Como Rodar o Projeto

O projeto é composto por **dois processos** que devem ser executados em terminais diferentes (ambos com o ambiente `(venv)` ativado):

1.  **🟢 Iniciar o Backend (API FastAPI):**
    O Backend deve ser iniciado primeiro. Deixe-o rodando no primeiro terminal:
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    *O console deve mostrar: `Cliente Gemini inicializado com sucesso!`*

2.  **🟢 Iniciar o Frontend (Streamlit):**
    O Frontend fornece a interface. Abra um segundo terminal (ATIVE O VENV!) e execute:
    ```bash
    python -m streamlit run app.py
    ```
    A interface web será aberta em `http://localhost:8501`.

---

## 🧪 Coleção de Testes (Demonstração do Contexto)

A documentação interativa (Swagger UI) está disponível em `http://127.0.0.1:8000/docs`.

Os testes em **`tests.http`** provam que o contexto é mantido e isolado, usando os usuários "pablo" e "maria". Você pode executar esses testes no VS Code usando a extensão REST Client.

| Teste | `user_id` | Mensagem Enviada | Prova de... |
| :---: | :---: | :--- | :--- |
| **Teste 2** | `pablo` | `O que são criptoativos?` | **Início de Sessão:** Inicia a sessão de Pablo. |
| **Teste 3** | `pablo` | `Qual é o principal risco disso?` | **Contexto Persistente:** A resposta é sobre os **riscos de criptoativos**. |
| **Teste 4** | `maria` | `Quais são as diferenças entre ações ordinárias e preferenciais?` | **Isolamento de Sessão:** A resposta é sobre **Ações** (ignora o contexto de Pablo). |
