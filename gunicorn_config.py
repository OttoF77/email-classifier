# Configuração do Gunicorn para Email Classifier
# Arquivo: gunicorn_config.py

import os
import multiprocessing

# Configurações básicas
port = int(os.environ.get("PORT", 8080))  # Porta do Render ou 8080 local
bind = f"0.0.0.0:{port}"  # Interface e porta dinâmica
workers = multiprocessing.cpu_count() * 2 + 1  # Número de workers baseado no CPU
worker_class = "sync"  # Classe do worker
worker_connections = 1000  # Conexões por worker

# Configurações de timeout
timeout = 120  # Timeout em segundos
keepalive = 5  # Keep-alive timeout

# Configurações de processo
max_requests = 1000  # Máximo de requests por worker antes de reiniciar
max_requests_jitter = 50  # Jitter para evitar restart simultâneo

# Configurações de memória
import platform
if platform.system() == "Linux":
    worker_tmp_dir = "/dev/shm"  # Usar RAM para arquivos temporários (Linux)
else:
    worker_tmp_dir = None  # Usar diretório padrão (macOS/Windows)
preload_app = True  # Pre-carrega a aplicação

# Configurações de log
accesslog = "-"  # Log de acesso no stdout
errorlog = "-"   # Log de erro no stderr
loglevel = "info"  # Nível de log
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configurações de segurança
user = None  # Usuário (definir em produção)
group = None  # Grupo (definir em produção)
umask = 0    # Permissões de arquivo

# Configurações de desenvolvimento (comentar em produção)
reload = False  # Auto-reload em mudanças de código
reload_extra_files = []  # Arquivos extras para monitorar

# Hook functions
def on_starting(server):
    """Executado quando o servidor inicia"""
    server.log.info("Email Classifier iniciando...")

def on_reload(server):
    """Executado quando o servidor recarrega"""
    server.log.info("Email Classifier recarregando...")

def on_exit(server):
    """Executado quando o servidor encerra"""
    server.log.info("Email Classifier encerrando...")

def worker_int(worker):
    """Executado quando worker recebe SIGINT"""
    worker.log.info("Worker interrompido pelo usuário")

def post_fork(server, worker):
    """Executado após fork do worker"""
    server.log.info("Worker iniciado com PID: %s", worker.pid)

def pre_fork(server, worker):
    """Executado antes do fork do worker"""
    pass

def worker_abort(worker):
    """Executado quando worker aborta"""
    worker.log.info("Worker abortado")

# Configurações específicas para Flask
raw_env = [
    'FLASK_ENV=production',
    'PYTHONPATH=/app'
]