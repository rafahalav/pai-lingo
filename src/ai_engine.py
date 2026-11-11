"""
Motor de IA do PAI - Lingo
Camada de negócio responsável pela integração com a Groq API.
"""

from groq import Groq
from groq import APIError, APIConnectionError, RateLimitError

from src.prompts import (
    CONVERSATION_PROMPT,
    GRAMMAR_PROMPT,
    VOCABULARY_PROMPT,
    EXERCISE_PROMPT,
    PRONUNCIATION_PROMPT,
)
from config import (
    GROQ_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    MAX_CONTEXT_MESSAGES,
)


class LingoAI:
    """
    Engine principal de IA para o PAI - Lingo.
    
    Encapsula a comunicação com a Groq API, aplicando os system prompts
    estruturados de cada modo de estudo e gerenciando o histórico de conversa.
    """
    
    # Mapeamento interno de modos → prompts
    _PROMPTS = {
        "conversation": CONVERSATION_PROMPT,
        "grammar": GRAMMAR_PROMPT,
        "vocabulary": VOCABULARY_PROMPT,
        "exercise": EXERCISE_PROMPT,
        "pronunciation": PRONUNCIATION_PROMPT,
    }
    
    def __init__(self, api_key: str):
        """
        Inicializa o cliente Groq.
        
        Args:
            api_key: Chave de API da Groq (obtida em console.groq.com)
        """
        self.client = Groq(api_key=api_key)
        self.model = GROQ_MODEL
    
    def _get_system_prompt(self, mode: str, **kwargs) -> str:
        """
        Retorna o system prompt formatado para o modo solicitado.
        
        Args:
            mode: Modo de estudo (conversation, grammar, vocabulary, exercise, pronunciation)
            **kwargs: Argumentos extras para formatação do prompt (ex: topic)
        
        Returns:
            System prompt pronto para ser enviado ao LLM
        """
        prompt_template = self._PROMPTS.get(mode)
        
        if prompt_template is None:
            # Fallback defensivo — nunca deve acontecer se o app.py estiver correto
            prompt_template = CONVERSATION_PROMPT
            kwargs.setdefault("topic", "general")
        
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            # Se faltar algum placeholder no kwargs, usa valor padrão
            raise ValueError(
                f"Prompt do modo '{mode}' requer argumento ausente: {e}"
            )
    
    def _trim_history(self, history: list) -> list:
        """
        Limita o histórico de mensagens para não estourar o contexto do LLM.
        
        Mantém apenas as últimas MAX_CONTEXT_MESSAGES mensagens, preservando
        a ordem cronológica.
        
        Args:
            history: Lista de mensagens no formato [{"role": ..., "content": ...}]
        
        Returns:
            Lista truncada (ou original, se já estiver dentro do limite)
        """
        if not history:
            return []
        
        if len(history) <= MAX_CONTEXT_MESSAGES:
            return history
        
        return history[-MAX_CONTEXT_MESSAGES:]
    
    def chat(
        self,
        user_message: str,
        mode: str = "conversation",
        conversation_history: list = None,
        **kwargs,
    ) -> str:
        """
        Envia uma mensagem ao LLM e retorna a resposta.
        
        Este é o método central da engine. Todos os outros métodos de
        conveniência delegam a ele.
        
        Args:
            user_message: Mensagem do usuário
            mode: Modo de estudo ativo
            conversation_history: Histórico de mensagens (opcional)
            **kwargs: Argumentos extras para o system prompt
        
        Returns:
            Resposta do LLM como string, ou mensagem de erro amigável
        """
        try:
            # Montar system prompt
            system_prompt = self._get_system_prompt(mode, **kwargs)
            
            # Montar lista de mensagens
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self._trim_history(conversation_history or []))
            messages.append({"role": "user", "content": user_message})
            
            # Chamada à API Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=TEMPERATURE.get(mode, 0.7),
                max_tokens=MAX_TOKENS,
            )
            
            return response.choices[0].message.content
        
        except RateLimitError:
            return (
                "⚠️ **Limite da API atingido.**\n\n"
                "Aguarde alguns segundos e tente novamente. "
                "Se o problema persistir, verifique seu plano em console.groq.com."
            )
        
        except APIConnectionError:
            return (
                "🌐 **Falha de conexão com a Groq API.**\n\n"
                "Verifique sua conexão com a internet e tente novamente."
            )
        
        except APIError as e:
            return (
                f"❌ **Erro na API Groq:**\n\n"
                f"`{e.status_code}` — {e.message}"
            )
        
        except ValueError as e:
            return f"⚙️ **Erro de configuração:** {str(e)}"
        
        except Exception as e:
            # Captura genérica — nunca deve chegar aqui em produção estável
            return (
                f"❌ **Erro inesperado:** {str(e)}\n\n"
                "Se o problema persistir, limpe a conversa e tente novamente."
            )
    
    # ============================================
    # MÉTODOS DE CONVENIÊNCIA
    # ============================================
    # Facilitam o uso direto de modos específicos sem precisar
    # passar o parâmetro `mode` manualmente.
    
    def correct_grammar(self, text: str) -> str:
        """Corrige gramática de um texto."""
        return self.chat(text, mode="grammar")
    
    def explain_vocabulary(self, word: str) -> str:
        """Explica uma palavra ou expressão."""
        return self.chat(word, mode="vocabulary")
    
    def generate_exercise(self, topic: str, level: str = "Intermediate") -> str:
        """Gera exercício interativo sobre um tópico."""
        return self.chat(
            f"Create an exercise about {topic} for {level} level.",
            mode="exercise",
        )
    
    def help_pronunciation(self, word: str) -> str:
        """Ajuda com a pronúncia de uma palavra ou frase."""
        return self.chat(word, mode="pronunciation")
    
    def converse(self, message: str, topic: str = "general", history: list = None) -> str:
        """Inicia ou continua uma conversação livre."""
        return self.chat(
            message,
            mode="conversation",
            conversation_history=history,
            topic=topic,
        )
