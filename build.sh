#!/bin/bash

# Email Classifier - Build & Production Script
# Este script consolida as funcionalidades de build, teste e deploy em produção

set -e  # Sair se qualquer comando falhar

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para mostrar ajuda
show_help() {
    echo "Email Classifier - Build & Production Script"
    echo ""
    echo "Uso: $0 [COMMAND]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  install     - Instalar dependências"
    echo "  test        - Executar testes"
    echo "  dev         - Executar em modo desenvolvimento"
    echo "  prod        - Executar em modo produção com Gunicorn"
    echo "  build       - Build completo (install + test)"
    echo "  deploy      - Deploy completo (build + prod)"
    echo "  stop        - Parar servidores em execução"
    echo "  status      - Verificar status dos serviços"
    echo "  help        - Mostrar esta ajuda"
    echo ""
}

# Função para instalar dependências
install_dependencies() {
    log "Instalando dependências..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v python3 &> /dev/null; then
            error "Python3 não encontrado. Instale primeiro o Python 3.8+"
            exit 1
        fi
    fi
    
    # Criar ambiente virtual se não existir
    if [ ! -d "venv" ]; then
        log "Criando ambiente virtual..."
        python3 -m venv venv
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências
    if [ -f "requirements.txt" ]; then
        log "Instalando dependências do requirements.txt..."
        pip install -r requirements.txt
    else
        error "requirements.txt não encontrado!"
        exit 1
    fi
    
    success "Dependências instaladas com sucesso!"
}

# Função para executar testes
run_tests() {
    log "Executando testes..."
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Executar testes com pytest
    if python3 -m pytest tests/ -v --tb=short; then
        success "Todos os testes passaram!"
        return 0
    else
        error "Alguns testes falharam!"
        return 1
    fi
}

# Função para executar em desenvolvimento
run_dev() {
    log "Iniciando servidor de desenvolvimento..."
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Configurar variáveis de ambiente para desenvolvimento
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    
    log "Servidor rodando em: http://localhost:5000"
    log "Pressione Ctrl+C para parar..."
    
    python3 run.py
}

# Função para executar em produção
run_production() {
    log "Iniciando servidor de produção com Gunicorn..."
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Verificar se Gunicorn está instalado
    if ! command -v gunicorn &> /dev/null; then
        warning "Gunicorn não encontrado. Instalando..."
        pip install gunicorn
    fi
    
    # Verificar se arquivo de configuração existe
    if [ ! -f "gunicorn_config.py" ]; then
        error "Arquivo gunicorn_config.py não encontrado!"
        exit 1
    fi
    
    # Configurar variáveis de ambiente para produção
    export FLASK_ENV=production
    export FLASK_DEBUG=0
    
    log "Servidor de produção rodando em: http://localhost:8080"
    log "Pressione Ctrl+C para parar..."
    
    # Executar Gunicorn
    python3 -m gunicorn --config gunicorn_config.py run:app
}

# Função para parar servidores
stop_servers() {
    log "Parando servidores..."
    
    # Parar processos Gunicorn
    pkill -f "gunicorn" 2>/dev/null || true
    
    # Parar processos Flask
    pkill -f "python3 run.py" 2>/dev/null || true
    
    success "Servidores parados!"
}

# Função para verificar status
check_status() {
    log "Verificando status dos serviços..."
    
    # Verificar Gunicorn
    if pgrep -f "gunicorn" > /dev/null; then
        success "Gunicorn está executando"
        echo "PIDs: $(pgrep -f 'gunicorn' | tr '\n' ' ')"
    else
        warning "Gunicorn não está executando"
    fi
    
    # Verificar Flask dev
    if pgrep -f "python3 run.py" > /dev/null; then
        success "Flask (dev) está executando"
        echo "PIDs: $(pgrep -f 'python3 run.py' | tr '\n' ' ')"
    else
        warning "Flask (dev) não está executando"
    fi
    
    # Verificar portas
    log "Verificando portas:"
    lsof -i :5000 2>/dev/null || echo "Porta 5000: Livre"
    lsof -i :8080 2>/dev/null || echo "Porta 8080: Livre"
}

# Função para build completo
full_build() {
    log "Iniciando build completo..."
    
    install_dependencies
    
    if run_tests; then
        success "Build completo executado com sucesso!"
    else
        error "Build falhou nos testes!"
        exit 1
    fi
}

# Função para deploy completo
full_deploy() {
    log "Iniciando deploy completo..."
    
    # Parar servidores existentes
    stop_servers
    
    # Executar build
    full_build
    
    # Executar em produção
    run_production
}

# Processamento dos argumentos da linha de comando
case "${1:-help}" in
    "install")
        install_dependencies
        ;;
    "test")
        run_tests
        ;;
    "dev")
        run_dev
        ;;
    "prod")
        run_production
        ;;
    "build")
        full_build
        ;;
    "deploy")
        full_deploy
        ;;
    "stop")
        stop_servers
        ;;
    "status")
        check_status
        ;;
    "help"|*)
        show_help
        ;;
esac