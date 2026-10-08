import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Carrega variáveis do arquivo .env
load_dotenv()

# Configuração da página do Streamlit
st.set_page_config(
    page_title="TourGuide AI - Assistente de Viagens",
    page_icon="✈️",
    layout="wide"
)

# Inicialização segura da API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Chave de API da Groq não encontrada. Configure no arquivo .env ou em .streamlit/secrets.toml")
    st.stop()

client = Groq(api_key=api_key)

# Título e cabeçalho
st.title("✈️ TourGuide AI")
st.subheader("Crie seu roteiro de viagem personalizado em segundos")

# Formulário para entrada do usuário
with st.form("form_agente"):
    col1, col2 = st.columns(2)
    
    with col1:
        destino = st.text_input("Para onde você quer ir?", placeholder="Ex: Roma, Itália")
        dias = st.number_input("Quantos dias vai durar a viagem?", min_value=1, max_value=30, value=3)
        
    with col2:
        estilo = st.selectbox(
            "Qual o seu estilo de viagem?",
            ["Econômico / Mochilão", "Cultural e Histórico", "Gastronômico", "Aventura e Natureza", "Luxo e Relaxamento"]
        )
        orcamento = st.selectbox(
            "Nível de orçamento:",
            ["Baixo", "Médio", "Alto"]
        )
        
    interesses_extras = st.text_area(
        "Interesses adicionais ou restrições (opcional):",
        placeholder="Ex: Viagem em família com crianças; prefiro lugares ao ar livre; opções vegetarianas."
    )
    
    submeter = st.form_submit_button("Gerar Roteiro de Viagem")

# Engenharia de Prompt e Chamada à API
SYSTEM_PROMPT = """
Você é o TourGuide AI, um especialista em turismo e planejamento de viagens globais.
Sua função é gerar roteiros completos, bem estruturados e práticos para os viajantes.

Regras de resposta:
1. Apresente um roteiro detalhado organizando por dias (Dia 1, Dia 2, etc.).
2. Para cada dia, inclua sugestões de manhã, tarde e noite.
3. Adicione uma seção de 'Dicas Gastronômicas' com pratos locais típicos.
4. Adicione uma seção de 'Informações Úteis' (transporte, melhor época para visitar, dicas de segurança).
5. Mantenha um tom acolhedor, profissional e motivador.
6. Use formatação Markdown (títulos, listas e negritos) para garantir leitura clara.
"""

if submeter:
    if not destino.strip():
        st.warning("Por favor, informe o destino desejado.")
    else:
        user_prompt = f"""
        Por favor, crie um roteiro de viagem com as seguintes características:
        - **Destino:** {destino}
        - **Duração:** {dias} dia(s)
        - **Estilo de Viagem:** {estilo}
        - **Orçamento:** {orcamento}
        - **Observações/Interesses Especiais:** {interesses_extras if interesses_extras else 'Nenhum'}
        """
        
        with st.spinner("O Agente está criando o seu roteiro personalizado..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b", # Modelo atualizado e funcional da Groq
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                roteiro = response.choices[0].message.content
                
                st.success("Roteiro gerado com sucesso!")
                st.markdown("---")
                st.markdown(roteiro)
                
            except Exception as e:
                st.error(f"Erro ao comunicar com o modelo da Groq: {e}")