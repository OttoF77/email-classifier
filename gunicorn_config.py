# Configuração do Gunicorn para Email Classifier - Render Optimized

import os

# Configurações básicas para Render
port = int(os.environ.get("PORT", 10000))  # Render usa porta 10000 por padrão
bind = f"0.0.0.0:{port}"  # Bind obrigatório para 0.0.0.0 no Render

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