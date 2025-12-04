# main.py 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.client import Chat 
import os
from typing import Dict, Optional

# Carrega variáveis de ambiente 
load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Instrução de sistema que define o papel do modelo Gemini
SYSTEM_INSTRUCTION = (
    "Você é um assistente especializado em finanças e investimentos, "
    "focado em fornecer análises, dicas de orçamento e explicações sobre termos e "
    "estratégias financeiras. Mantenha um tom profissional e informativo."
)

client: Optional[genai.Client] = None
# Dicionário global para armazenar as sessões de chat. 
# A chave é o user_id e o valor é a instância Chat, mantendo o contexto conversacional.
CHAT_SESSIONS: Dict[str, Chat] = {} # <--- CORRIGIDO: Usa a classe Chat importada

if GEMINI_API_KEY:
    try:
        # Inicializa o cliente Gemini com a chave de API
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("Cliente Gemini inicializado com sucesso!")
    except Exception as e:
        print(f"ERRO: Não foi possível inicializar o cliente Gemini. Detalhe: {e}")
        client = None
else:
    print("AVISO: Chave GEMINI_API_KEY não encontrada. O serviço de IA estará indisponível.")


# Modelo Pydantic para a requisição de chat (validação de entrada)
class ChatRequest(BaseModel):
    # user_id para identificar o usuário e recuperar seu contexto
    user_id: str = Field(..., example="Pablo")
    message: str = Field(..., example="Qual a diferença entre LCI e LCA?")
    
# Modelo Pydantic para a resposta de chat (estruturação da saída)
class ChatResponse(BaseModel):
    response: str = Field(..., example="LCI e LCA são títulos de renda fixa isentos de Imposto de Renda, lastreados, respectivamente, nos setores imobiliário e do agronegócio.")
    source_model: str = "Gemini-2.5-Flash (Especialista Financeiro)"

app = FastAPI(
    title="💰 J.A.R.V.I.S - Assistente financeiro",
    description="API para um assistente que ajuda com conceitos financeiros, integrada ao Google Gemini e com contexto por usuário.",
    version="1.0.0",
)

# Rota de saúde simples, gera a documentação do Swagger em /docs
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Assistente LLM pronto. Acesse /docs para a documentação interativa."}

# Rota principal para processar mensagens do chat
@app.post("/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    # Verifica a disponibilidade do cliente de IA (tratamento de erro 503)
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Serviço de IA indisponível. Verifique sua chave de API ou conexão.",
        )

    user_id = request.user_id
    
    # Lógica para gerenciar o contexto conversacional por usuário
    if user_id not in CHAT_SESSIONS:
        try:
            # Cria uma nova sessão de chat (com histórico vazio) e aplica a SYSTEM_INSTRUCTION
            chat_session = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION
                )
            )
            CHAT_SESSIONS[user_id] = chat_session
            print(f"Nova sessão de chat criada para o usuário: {user_id}")
        except Exception as e:
            print(f"Erro ao criar nova sessão de chat: {e}")
            # Erro interno na criação da sessão (tratamento de erro 500)
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao iniciar a sessão de IA.",
            )
    else:
        # Recupera a sessão existente para continuar a conversa (manter o contexto)
        chat_session = CHAT_SESSIONS[user_id]

    try:
        # Envia a mensagem do usuário para a sessão de chat, que inclui o histórico anterior
        response = chat_session.send_message(request.message)

        # Retorna a resposta estruturada em JSON
        return ChatResponse(
            response=response.text,
            source_model="Gemini-2.5-Flash (Especialista Financeiro)"
        )

    except Exception as e:
        print(f"Erro na comunicação com a API Gemini: {e}")
        # Erro interno durante a comunicação com a API (tratamento de erro 500)
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar a requisição com o modelo de IA.",
        )

if __name__ == "__main__":
    # Inicializa o servidor Uvicorn para rodar o FastAPI
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
