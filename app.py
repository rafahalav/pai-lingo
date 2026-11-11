"""
PAI - Lingo - Personal Assistente de Inglês
Aplicação principal Streamlit
"""

import streamlit as st
from dotenv import load_dotenv
import os
from src.ai_engine import LingoAI
from src.utils import save_conversation_history, load_conversation_history

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="PAI - Lingo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - Identidade visual
st.markdown("""
<style>
    /* Header principal */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #1e3a8a !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] h4 {
        color: #1e3a8a !important;
        font-weight: 600;
    }
    
    /* Texto em itálico (em) na sidebar */
    [data-testid="stSidebar"] em {
        color: #1e3a8a !important;
        font-style: italic;
    }
    
    /* FORÇAR COR AZUL EM TODOS OS LABELS DA SIDEBAR */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio > div > label,
    [data-testid="stSidebar"] .stRadio > div > label > div,
    [data-testid="stSidebar"] .stRadio > div > label > div > p {
        color: #1e3a8a !important;
        font-weight: 500 !important;
    }
    
    /* Hover nos radio buttons */
    [data-testid="stSidebar"] .stRadio label:hover,
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        color: #0891b2 !important;
    }
    
    /* 1. CAIXA API KEY - TRANSPARENTE COM TEXTO AZUL (apenas input) */
    [data-testid="stSidebar"] {
        background-color: transparent !important;
        color: #1e3a8a !important;
        border: 1px solid #1e3a8a !important;
        border-radius: 8px !important;
    }
    
    /* 2. CAIXA TEMA DA CONVERSA - TRANSPARENTE COM TEXTO LARANJA */
    [data-testid="stSidebar"] input[type="text"] {
        background-color: transparent !important;
        color: #f97316 !important;
        border: 1px solid #f97316 !important;
        border-radius: 8px !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
    }
    
    /* Botões */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Radio buttons */
    .stRadio > div {
        padding: 0.5rem 0;
    }
    
    .stRadio > div > label {
        padding: 0.5rem;
        border-radius: 6px;
        transition: background 0.2s;
    }
    
    .stRadio > div > label:hover {
        background: rgba(102, 126, 234, 0.1);
    }
</style>

<script>
// Aguardar o DOM carregar e aplicar estilos aos botões
setTimeout(function() {
    // Encontrar todos os botões na sidebar
    var sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        var buttons = sidebar.querySelectorAll('button');
        buttons.forEach(function(btn) {
            var btnText = btn.innerText.trim();
            
            // Botão "Limpar" - Vermelho
            if (btnText.includes('Limpar')) {
                btn.style.backgroundColor = 'transparent';
                btn.style.color = '#dc2626';
                btn.style.border = '1px solid #dc2626';
                btn.style.borderRadius = '8px';
            }
            // Botão "Exportar" - Azul
            else if (btnText.includes('Exportar')) {
                btn.style.backgroundColor = 'transparent';
                btn.style.color = '#1e3a8a';
                btn.style.border = '1px solid #1e3a8a';
                btn.style.borderRadius = '8px';
            }
            // Botão "Baixar" - Azul
            else if (btnText.includes('Baixar')) {
                btn.style.backgroundColor = 'transparent';
                btn.style.color = '#1e3a8a';
                btn.style.border = '1px solid #1e3a8a';
                btn.style.borderRadius = '8px';
            }
        });
    }
}, 1000);

// Observar mudanças no DOM para aplicar estilos quando o botão "Baixar" aparecer
var observer = new MutationObserver(function(mutations) {
    var sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        var buttons = sidebar.querySelectorAll('button');
        buttons.forEach(function(btn) {
            var btnText = btn.innerText.trim();
            
            if (btnText.includes('Baixar')) {
                btn.style.backgroundColor = 'transparent';
                btn.style.color = '#1e3a8a';
                btn.style.border = '1px solid #1e3a8a';
                btn.style.borderRadius = '8px';
            }
        });
    }
});

observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# Inicialização de estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = load_conversation_history()
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "conversation"
if "conversation_topic" not in st.session_state:
    st.session_state.conversation_topic = "general"

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    # Logo/Ícone
    st.image("https://img.icons8.com/fluency/96/language.png", width=80)
    
    # Título da sidebar
    st.markdown("### 🎓 PAI - Lingo")
    st.markdown("*Personal Assistente de Inglês*")
    st.markdown("---")
    
    # Configuração da API Key
    st.markdown("#### 🔐 Autenticação")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Obtenha sua chave em: https://console.groq.com"
    )
    
    if not api_key:
        st.warning("⚠️ Insira sua Groq API Key para começar")
        st.stop()
    
    st.markdown("---")
    
    # Seleção de Modo
    st.markdown("#### 📚 Modo de Estudo")
    mode = st.radio(
        "Escolha o modo:",
        [
            "💬 Conversação Livre",
            "✍️ Correção Gramatical",
            "📖 Vocabulário",
            "📝 Exercícios",
            "📣 Pronúncia"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    # Mapear modo para código interno
    mode_map = {
        "💬 Conversação Livre": "conversation",
        "✍️ Correção Gramatical": "grammar",
        "📖 Vocabulário": "vocabulary",
        "📝 Exercícios": "exercise",
        "📣 Pronúncia": "pronunciation"
    }
    st.session_state.current_mode = mode_map[mode]
    
    # Campo de tópico (apenas para conversação)
    if st.session_state.current_mode == "conversation":
        st.markdown("#### 🤔 Tópico (opcional)")
        topic = st.text_input(
            "Tema da conversa:",
            value="general",
            help="Ex: travel, business, technology, daily life"
        )
        st.session_state.conversation_topic = topic
    
    st.markdown("---")
    
    # Ações
    st.markdown("#### ⚙️ Ações")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.messages = []
            save_conversation_history([])
            st.rerun()
    
    with col2:
        if st.button("📋 Exportar", use_container_width=True):
            # Exportar conversa como texto
            conversation_text = "\n\n".join([
                f"{'USUÁRIO' if m['role'] == 'user' else 'TUTOR'}: {m['content']}"
                for m in st.session_state.messages
            ])
            st.download_button(
                "⬇️ Baixar",
                conversation_text,
                file_name="pai_lingo_conversation.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
        "Desenvolvido por <strong>Rafael Halav</strong><br>"
        "<small>PAI Series • 2026</small>"
        "</div>",
        unsafe_allow_html=True
    )

# ============================================
# HEADER PRINCIPAL
# ============================================
st.markdown('<div class="main-header">🎓 🇧🇷 PAI - Lingo 🇺🇸</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Personal Assistant de Inglês • Seu tutor pessoal de idiomas</div>',
    unsafe_allow_html=True
)

# Indicador de modo atual
mode_descriptions = {
    "conversation": "💬 Pratique conversação natural em inglês",
    "grammar": "✍️ Envie textos para análise gramatical detalhada",
    "vocabulary": "💻️ Digite palavras ou frases para aprender",
    "exercise": "📝 Gere exercícios personalizados",
    "pronunciation": "🔊 Aprenda a pronúncia correta"
}

st.info(mode_descriptions[st.session_state.current_mode])

# ============================================
# IMPORTS DA ENGINE (após API key validada)
# ============================================
from src.ai_engine import LingoAI

# Inicializar engine
ai = LingoAI(api_key)

# ============================================
# CHAT INTERFACE
# ============================================

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem em inglês..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gerar resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("🤔 Pensando..."):
            try:
                # Preparar argumentos extras baseado no modo
                kwargs = {}
                if st.session_state.current_mode == "conversation":
                    kwargs["topic"] = st.session_state.conversation_topic
                
                response = ai.chat(
                    prompt,
                    mode=st.session_state.current_mode,
                    conversation_history=st.session_state.messages[:-1],
                    **kwargs
                )
                st.markdown(response)
            except Exception as e:
                response = f"❌ Erro ao processar requisição: {str(e)}"
                st.error(response)
    
    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_conversation_history(st.session_state.messages) 
