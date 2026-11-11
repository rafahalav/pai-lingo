#!/bin/bash

# ============================================================================
# PAI - Lingo - Script de Inicialização
# Personal Assistant de Inglês
# ============================================================================

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Nome do ambiente virtual
ENV_NAME="pai-lingo"

echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          🎓 PAI - Lingo - Iniciando...              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se micromamba está instalado
if ! command -v micromamba &> /dev/null; then
    echo -e "${RED}❌ Erro: micromamba não encontrado!${NC}"
    echo -e "${YELLOW}Instale o micromamba primeiro: https://mamba.readthedocs.io/${NC}"
    exit 1
fi

# Verificar se o ambiente virtual existe
if micromamba env list | grep -q "$ENV_NAME"; then
    echo -e "${GREEN}✅ Ambiente virtual encontrado: $ENV_NAME${NC}"
else
    echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado. Criando...${NC}"
    micromamba create --name $ENV_NAME python=3.13 -y
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Ambiente criado com sucesso!${NC}"
    else
        echo -e "${RED}❌ Erro ao criar ambiente virtual${NC}"
        exit 1
    fi
fi

# Verificar/atualizar dependências DENTRO do ambiente
echo -e "${BLUE}📦 Verificando dependências...${NC}"
micromamba run -n $ENV_NAME pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências verificadas/atualizadas${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi

# Verificar arquivo .env
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ Arquivo .env encontrado${NC}"
else
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
    echo -e "${YELLOW}   Lembre-se de criar o arquivo .env com sua GROQ_API_KEY${NC}"
fi

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 Iniciando Streamlit...                          ║${NC}"
echo -e "${BLUE}║  Acesse: http://localhost:8501                      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# Iniciar Streamlit DENTRO do ambiente (sem precisar de activate)
micromamba run -n $ENV_NAME streamlit run app.py
