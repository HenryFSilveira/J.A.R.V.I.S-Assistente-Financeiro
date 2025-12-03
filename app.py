# ARQUIVO: app.py
import streamlit as st
import requests
import json
import uuid

# --- Configurações da Aplicação ---
st.set_page_config(
    page_title="💰 J.A.R.V.I.S - Assistente financeiro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# A URL onde sua API FastAPI está rodando
API_URL = "http://localhost:8000/chat" 

# 1. Gera um ID de usuário persistente para manter o contexto conversacional
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
    print(f"Novo usuário iniciado com ID: {st.session_state.user_id}")

# 2. Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas inicial do assistente
    st.session_state.messages.append(
        {"role": "assistant", "content": "Olá! Eu me chamo J.A.R.V.I.S, serei seu assistente financeiro. Como posso ajudar você com suas finanças?"}
    )

# --- Funções de Comunicação com a API ---

def send_message_to_api(message: str, user_id: str):
    """Envia a mensagem para a API FastAPI e retorna a resposta da IA."""
    try:
        # Prepara o payload JSON, incluindo o user_id
        payload = {
            "user_id": user_id,
            "message": message
        }
        
        # Faz a requisição POST para o seu backend
        response = requests.post(API_URL, json=payload, timeout=30)
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Erro: Resposta vazia da IA.")
        else:
            # Captura erros de HTTP (ex: 503 Serviço Indisponível)
            error_detail = response.json().get("detail", f"Erro HTTP {response.status_code}")
            return f"❌ Erro ao comunicar com a API: {error_detail}"

    except requests.exceptions.ConnectionError:
        return "❌ Erro de Conexão: Certifique-se de que sua API FastAPI (`main.py`) está rodando em " + API_URL
    except Exception as e:
        return f"❌ Erro inesperado: {e}"

# --- Estrutura da Interface Streamlit ---

st.title("💰 J.A.R.V.I.S - Assistente financeiro")
st.caption(f"ID da Sessão: {st.session_state.user_id[:8]}...")
st.markdown("---")

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Pergunte algo sobre finanças ou investimentos..."):
    
    # 1. Adiciona a mensagem do usuário ao histórico do Streamlit
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Usa um placeholder para mostrar que a IA está pensando
    with st.chat_message("assistant"):
        with st.spinner("Analisando sua questão..."):
            
            # 3. Chama a função que se comunica com a API FastAPI
            full_response = send_message_to_api(prompt, st.session_state.user_id)
            
            # 4. Exibe a resposta final e a adiciona ao histórico
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})