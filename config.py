"""
Configurações globais do PAI - Lingo
Centraliza parâmetros do modelo, temperaturas e constantes da aplicação.
"""

# ============================================
# MODELO GROQ
# ============================================
GROQ_MODEL = "openai/gpt-oss-120b"

# ============================================
# TEMPERATURAS POR MODO
# ============================================
# Controle de criatividade do LLM por tipo de interação
# Quanto menor, mais determinístico e preciso
# Quanto maior, mais criativo e variado
TEMPERATURE = {
    "conversation": 0.7,    # Naturalidade e fluidez
    "grammar": 0.3,         # Precisão máxima
    "vocabulary": 0.5,      # Equilíbrio entre precisão e criatividade
    "exercise": 0.6,        # Variedade nos exercícios
    "pronunciation": 0.4    # Consistência fonética
}

# ============================================
# LIMITES DE TOKENS
# ============================================
MAX_TOKENS = 2000           # Limite por resposta
MAX_CONTEXT_MESSAGES = 20   # Máximo de mensagens no histórico

# ============================================
# CONFIGURAÇÕES DE INTERFACE
# ============================================
DEFAULT_MODE = "conversation"
DEFAULT_TOPIC = "general"

# ============================================
# MAPEAMENTO DE MODOS
# ============================================
MODE_MAP = {
    "💬 Conversação Livre": "conversation",
    "✍️ Correção Gramatical": "grammar",
    "📚 Vocabulário": "vocabulary",
    "🎯 Exercícios": "exercise",
    "🔊 Pronúncia": "pronunciation"
}

# Descrições dos modos para exibição na UI
MODE_DESCRIPTIONS = {
    "conversation": "💬 Pratique conversação natural em inglês",
    "grammar": "✍️ Envie textos para análise gramatical detalhada",
    "vocabulary": "📚 Digite palavras ou frases para aprender",
    "exercise": "🎯 Gere exercícios personalizados",
    "pronunciation": "🔊 Aprenda a pronúncia correta"
}
