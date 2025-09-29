# Configuração do Gunicorn para Email Classifier - Render Optimized

import os

# Forçar logs para garantir que o config está sendo carregado
import sys
print(f"🔧 [GUNICORN CONFIG] ===== CARREGANDO CONFIGURAÇÃO CUSTOMIZADA =====", file=sys.stderr)
print(f"🔧 [GUNICORN CONFIG] PORT environment: {os.environ.get('PORT', 'NOT SET')}", file=sys.stderr)

# Configurações básicas para Render
port = int(os.environ.get("PORT", 10000))  # Render usa porta 10000 por padrão
bind = f"0.0.0.0:{port}"  # Bind obrigatório para 0.0.0.0 no Render

print(f"🔧 [GUNICORN CONFIG] Bind configurado para: {bind}", file=sys.stderr)
print(f"🔧 [GUNICORN CONFIG] Workers: 2, Timeout: 300s", file=sys.stderr)
print(f"🔧 [GUNICORN CONFIG] ===== CONFIGURAÇÃO CUSTOMIZADA CARREGADA =====", file=sys.stderr)

# Workers - configuração conservadora para Render
workers = 2  # Número fixo para evitar problemas de memória
worker_class = "sync"
worker_connections = 1000

# Timeouts aumentados para AI/ML processing
timeout = 300  # 5 minutos - AI processing pode demorar
keepalive = 10
graceful_timeout = 30

# Configurações de requests
max_requests = 500  # Menor para economizar memória  
max_requests_jitter = 25

# Configurações otimizadas para Render
preload_app = True
worker_tmp_dir = "/dev/shm"  # RAM disk no Linux/Render

# Logs simples
accesslog = "-"  # stdout
errorlog = "-"   # stderr  
loglevel = "info"

# Configurações de produção
reload = False
user = None
group = None