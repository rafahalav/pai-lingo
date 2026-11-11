
# 🎓 PAI - Lingo

**Personal Assistant de Inglês** — Tutor inteligente de idiomas com Engenharia de Prompt aplicada ao ensino.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49.1-FF4B4B?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F55036?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciLz4=)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 🚀 Sobre o Projeto

O **PAI - Lingo** não é um chatbot de tradução genérico. É uma aplicação web interativa projetada com **Engenharia de Prompt pedagógica** para atuar como um tutor pessoal de inglês em cinco modalidades especializadas de estudo.

Cada modo de interação possui um *system prompt* estruturado com objetivos didáticos claros, garantindo que o LLM se comporte como um professor — não como um assistente de propósito geral. A saída é padronizada, mensurável e alinhada a boas práticas de **AI Training**, facilitando futuras iterações com RLHF (Reinforcement Learning from Human Feedback).

Este projeto faz parte da **série PAI (Personal Assistants of Intelligence)**, desenvolvida como parte da minha transição profissional para Inteligência Artificial e Desenvolvimento de Software, aplicando 25+ anos de experiência em infraestrutura, lógica e educação técnica.

---

## 📚️️ Arquitetura Pedagógica

O diferencial do 🎓️ PAI - Lingo está na **separação pedagógica por modo**. Cada modalidade de estudo possui:

| Modo | Objetivo Pedagógico | Temperatura |
|------|---------------------|:-----------:|
| 💬 **Conversação Livre** | Fluência e naturalidade | 0.7 |
| ✍️ **Correção Gramatical** | Precisão e análise estrutural | 0.3 |
| 📖 **Vocabulário** | Aquisição lexical contextual | 0.5 |
| 📝 **Exercícios** | Fixação ativa do conhecimento | 0.6 |
| 📣 **Pronúncia** | Consciência fonológica | 0.4 |

A variação controlada de temperatura por modo é uma decisão técnica intencional: modos que exigem precisão (gramática, pronúncia) operam com baixa entropia; modos que exigem criatividade (conversação, exercícios) operam com entropia maior.

---

## ✨ Destaques Técnicos

### Engenharia de Prompt Estruturada
Cada modo possui um *system prompt* dedicado com:
- **Papel definido** (tutor, revisor, coach)
- **Estrutura de saída padronizada** (facilita avaliação humana)
- **Diretrizes pedagógicas explícitas** (evita alucinações e desvios)
- **Controle de tom** (encorajador, técnico, direto)

### Prontidão para RLHF
A saída estruturada permite avaliação humana consistente da qualidade das respostas, simulando fluxos de trabalho reais de treinamento de modelos de linguagem.

### Gerenciamento de Estado
Uso de `st.session_state` para manter contexto conversacional fluido entre interações, com limite configurável de mensagens no histórico (`MAX_CONTEXT_MESSAGES`).

### Separação de Responsabilidades
Arquitetura modular seguindo princípios SOLID:
- `app.py` → Camada de apresentação
- `src/ai_engine.py` → Camada de negócio (integração LLM)
- `src/prompts.py` → Camada de conhecimento (prompts)
- `src/utils.py` → Funções auxiliares
- `config.py` → Configurações centralizadas

### Tratamento de Erros Robusto
Blocos `try/except` em todas as chamadas de API, garantindo que falhas de rede ou limites de tokens não quebrem a aplicação — apenas orientam o usuário.

### Segurança
A chave de API é inserida dinamicamente via interface ou variáveis de ambiente (`.env`), nunca hardcoded no repositório. O arquivo `.gitignore` protege credenciais.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Linguagem | Python 3.13 | Tipagem moderna, performance |
| Framework Web | Streamlit 1.49.1 | Prototipagem rápida, foco em dados |
| Inferência LLM | Groq API | Alta velocidade, baixa latência |
| Gerenciamento | Micromamba | Ambientes leves e isolados |
| Segurança | python-dotenv | Separação de credenciais |

---

## ⚙️ Instalação e Uso Local

### 🛠️ Método Padrão (Recomendado)

Siga os passos convencionais para configurar o ambiente de desenvolvimento:

1. **Navegue até o diretório do projeto:**
   ```bash
   cd ~/CYBERDECK/12_PROJECTS/pai-lingo
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   micromamba create --name pai-lingo python=3.13 -y
   micromamba activate pai-lingo
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```
   Acesse em: `http://localhost:8501`

> **Nota de Segurança:** Insira sua chave da Groq API no campo dedicado na barra lateral da aplicação, ou configure um arquivo `.env` localmente na raiz do projeto:
> ```env
> GROQ_API_KEY=sua_chave_aqui
> ```

---

### 🚀 Método Rápido (Opcional via Script)

Como conveniência, o projeto inclui um script de inicialização automatizada (`start.sh`) que gerencia o ambiente e as dependências automaticamente.

1. **Torne o script executável (apenas na primeira vez):**
   ```bash
   chmod +x start.sh
   ```
2. **Execute o script:**
    ```bash
    .start.sh
    ```
    
---

## 📁 Estrutura do Projeto

```text
pai-lingo/
├── app.py                 # Entry point — camada de apresentação
├── config.py              # Configurações globais centralizadas
├── start.sh               # Script de inicialização automatizada (Bash)
├── requirements.txt       # Dependências do projeto
├── README.md              # Esta documentação
├── .env                   # Variáveis de ambiente (não versionado)
├── .gitignore             # Regras de exclusão do Git
├── src/
│   ├── __init__.py
│   ├── ai_engine.py       # Integração com Groq API
│   ├── prompts.py         # System prompts estruturados por modo
│   └── utils.py           # Funções auxiliares
└── assets/                # Recursos estáticos (ícones, imagens)
```

---

## 💬 Exemplos de Interação

### ✍️ Correção Gramatical

**Usuário:** *"I goes to school yesterday with my friends."*

**PAI - Lingo:**
> **Original Text:** I goes to school yesterday with my friends.
> 
> **Corrected Version:** I went to school yesterday with my friends.
> 
> **Grammar Analysis:**
> - *goes* → *went*: o verbo deve estar no *simple past* pois a ação ocorreu em tempo definido (*yesterday*).
> 
> **Practice Tip:** Quando houver marcadores temporais como *yesterday*, *last week*, *in 2020*, use sempre o *simple past*.

---

### 📖 Vocabulário

**Usuário:** *"serendipity"*

**PAI - Lingo:**
> **Word:** serendipity
> **Pronunciation:** /ˌser.ənˈdɪp.ə.ti/
> **Translation (PT-BR):** acaso feliz, descoberta afortunada
> 
> **Definition:** The occurrence of events by chance in a happy or beneficial way.
> 
> **Examples:**
> 1. *Finding that book was pure serendipity.*
> 2. *Many scientific discoveries were the result of serendipity.*

---

### 📝 Exercícios

**Usuário:** *"Crie um exercício sobre phrasal verbs com 'get'."*

**PAI - Lingo:** gera um quiz interativo com fill-in-the-blank, múltipla escolha e gabarito comentado.

---

## 🗺️ Roadmap

- [ ] Sistema de flashcards integrado para vocabulário
- [ ] Text-to-speech real (gTTS) para modo pronúncia
- [ ] Speech-to-text para prática de conversação por voz
- [ ] Histórico persistente de conversas (SQLite)
- [ ] Estatísticas de progresso do aprendiz
- [ ] Exportação de sessões em PDF

---

## 🧑‍💻 Autor

**Rafael Halav**
*Technology Professional | Telecommunications | IT | Python | AI | Data*

🔗 [LinkedIn](https://www.linkedin.com/in/rafael-halav-tech) · ✉️ [Contato](mailto:rafael.halav.tech@gmail.com)

---

*Desenvolvido com foco em aprendizado contínuo e aplicação prática de Inteligência Artificial.*

**PAI Series • 2026**
```
