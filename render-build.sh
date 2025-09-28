#!/bin/bash

# Script de build para Render.com
# Este script é executado durante o processo de build no Render

set -e

echo "🚀 Iniciando build para Render..."

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python não encontrado!"
    exit 1
fi

echo "🐍 Usando $PYTHON_CMD $(${PYTHON_CMD} --version)"

# Atualizar pip
$PYTHON_CMD -m pip install --upgrade pip

echo "📦 Instalando dependências..."
$PYTHON_CMD -m pip install -r requirements.txt

echo "🔍 Verificando instalação das dependências críticas..."
$PYTHON_CMD -c "import flask; print('✅ Flask instalado')"
$PYTHON_CMD -c "import gunicorn; print('✅ Gunicorn instalado')"
$PYTHON_CMD -c "import transformers; print('✅ Transformers instalado')"
$PYTHON_CMD -c "import psycopg2; print('✅ PostgreSQL driver instalado')"

echo "🗄️ Configurando banco de dados..."
# Executar migrações se necessário
if [ ! -z "$DATABASE_URL" ]; then
    echo "Executando migrações do banco..."
    $PYTHON_CMD -c "from app import create_app; from flask_migrate import upgrade; app = create_app(); app.app_context().push(); upgrade()"
else
    echo "⚠️ DATABASE_URL não configurado - pulando migrações"
fi

echo "🧪 Executando testes básicos..."
$PYTHON_CMD -c "from app import create_app; app = create_app(); print('✅ App Flask criado com sucesso')"

echo "🎯 Verificando configuração do Gunicorn..."
$PYTHON_CMD -c "import gunicorn_config; print('✅ Configuração Gunicorn carregada')"

echo "✅ Build concluído com sucesso!"
echo "🌐 Aplicação pronta para deploy!"