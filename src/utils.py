"""
Funções auxiliares do PAI - Lingo.

Contém utilitários para processamento de texto, detecção de idioma,
extração de palavras-chave e formatações diversas.
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """
    Limpa e normaliza texto.
    
    Remove espaços extras, quebras de linha desnecessárias e caracteres
    de controle.
    
    Args:
        text: Texto a ser limpo
    
    Returns:
        Texto limpo e normalizado
    """
    if not text:
        return ""
    
    # Remove espaços extras (mantém apenas um espaço entre palavras)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove quebras de linha múltiplas (mantém no máximo uma)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def detect_language(text: str) -> str:
    """
    Detecta se o texto está predominantemente em inglês ou português.
    
    Usa heurística simples baseada em palavras comuns de cada idioma.
    Não é 100% preciso, mas suficiente para o contexto do PAI - Lingo.
    
    Args:
        text: Texto para análise
    
    Returns:
        'en-US' se predominantemente inglês, 'pt-BR' se predominantemente português
    """
    if not text:
        return "en-US"
    
    # Palavras muito comuns em português (artigos, preposições, conjunções)
    pt_indicators = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
        'de', 'da', 'do', 'das', 'dos',
        'em', 'na', 'no', 'nas', 'nos',
        'por', 'pela', 'pelo', 'pelas', 'pelos',
        'para', 'pra',
        'com', 'sem',
        'sob', 'sobre',
        'até', 'após',
        'desde', 'entre',
        'que', 'quem',
        'qual', 'quais',
        'cujo', 'cuja',
        'e', 'mas', 'porém', 'todavia', 'contudo', 'entretanto',
        'se', 'caso', 'quando', 'enquanto', 'logo', 'portanto',
        'sim', 'não', 'talvez',
        'muito', 'pouco', 'bastante',
        'aqui', 'ali', 'lá', 'cá',
        'hoje', 'ontem', 'amanhã',
        'eu', 'você', 'ele', 'ela', 'nós', 'eles', 'elas',
        'meu', 'minha', 'teu', 'tua', 'seu', 'sua',
        'este', 'esta', 'esse', 'essa', 'aquele', 'aquela',
    }
    
    # Palavras muito comuns em inglês
    en_indicators = {
        'the', 'a', 'an',
        'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'from',
        'and', 'or', 'but', 'so', 'yet', 'nor',
        'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'having',
        'do', 'does', 'did', 'doing',
        'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
        'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'its', 'our', 'their',
        'this', 'that', 'these', 'those',
        'what', 'which', 'who', 'whom', 'whose',
        'when', 'where', 'why', 'how',
        'not', 'no', 'yes',
        'very', 'too', 'quite', 'rather',
        'here', 'there', 'now', 'then',
        'today', 'yesterday', 'tomorrow',
    }
    
    # Tokenizar texto (palavras em minúsculo)
    words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return "en-US"
    
    # Contar indicadores
    pt_count = sum(1 for word in words if word in pt_indicators)
    en_count = sum(1 for word in words if word in en_indicators)
    
    # Se tem mais indicadores de português que inglês, assume português
    if pt_count > en_count:
        return "pt-BR"
    
    return "en-US"


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extrai palavras-chave de um texto.
    
    Remove stopwords básicas e palavras muito curtas.
    
    Args:
        text: Texto para análise
        min_length: Comprimento mínimo das palavras (padrão: 3)
    
    Returns:
        Lista de palavras-chave únicas
    """
    if not text:
        return []
    
    # Stopwords básicas (inglês + português)
    stopwords = {
        # Inglês
        'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by',
        'from', 'and', 'or', 'but', 'so', 'is', 'are', 'was', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
        'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'this',
        'that', 'these', 'those', 'what', 'which', 'who', 'whom', 'whose',
        'when', 'where', 'why', 'how', 'not', 'no', 'yes',
        # Português
        'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos',
        'em', 'na', 'no', 'nas', 'nos', 'por', 'para', 'com', 'sem', 'e',
        'mas', 'que', 'se', 'eu', 'você', 'ele', 'ela', 'nós', 'eles', 'elas',
        'me', 'te', 'meu', 'minha', 'seu', 'sua', 'este', 'esta', 'esse', 'essa',
    }
    
    # Extrair palavras
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filtrar
    keywords = [
        word for word in words
        if word not in stopwords and len(word) >= min_length
    ]
    
    # Retornar únicas (preservando ordem)
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)
    
    return unique_keywords


def format_conversation_for_export(messages: List[dict]) -> str:
    """
    Formata histórico de conversa para exportação em texto.
    
    Args:
        messages: Lista de mensagens no formato [{"role": ..., "content": ...}]
    
    Returns:
        Texto formatado para exportação
    """
    if not messages:
        return "Nenhuma mensagem na conversa."
    
    lines = []
    for msg in messages:
        role = "USUÁRIO" if msg["role"] == "user" else "TUTOR"
        content = msg["content"]
        lines.append(f"{role}:\n{content}\n")
    
    return "\n".join(lines)


def count_words(text: str) -> int:
    """
    Conta o número de palavras em um texto.
    
    Args:
        text: Texto para análise
    
    Returns:
        Número de palavras
    """
    if not text:
        return 0
    
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Trunca texto se exceder comprimento máximo.
    
    Args:
        text: Texto para truncar
        max_length: Comprimento máximo (padrão: 100)
        suffix: Sufixo a adicionar se truncado (padrão: "...")
    
    Returns:
        Texto truncado ou original
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].rstrip() + suffix

import json
from pathlib import Path


def save_conversation_history(messages: List[dict], filepath: str = "history.json") -> None:
    """
    Salva o histórico de conversa em arquivo JSON.
    
    Args:
        messages: Lista de mensagens no formato [{"role": ..., "content": ...}]
        filepath: Caminho do arquivo JSON (padrão: "history.json" na raiz do projeto)
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")


def load_conversation_history(filepath: str = "history.json") -> List[dict]:
    """
    Carrega o histórico de conversa de arquivo JSON.
    
    Args:
        filepath: Caminho do arquivo JSON (padrão: "history.json" na raiz do projeto)
    
    Returns:
        Lista de mensagens ou lista vazia se o arquivo não existir
    """
    try:
        path = Path(filepath)
        if path.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
    
    return []
