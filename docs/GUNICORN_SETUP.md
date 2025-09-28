# 🚀 Gunicorn - Servidor de Produção para Email Classifier

## 📋 **Resumo**

O **Gunicorn** (Green Unicorn) foi instalado e configurado como servidor WSGI para executar a aplicação Email Classifier em ambiente de produção.

---

## ✅ **Instalação Concluída**

### **Dependências Instaladas:**
```bash
gunicorn==23.0.0
```

### **Arquivos Criados:**
- `gunicorn_config.py` - Configuração detalhada do servidor
- `build.sh` - Script consolidado para build e produção
- `run.py` - Modificado para expor a variável `app`

---

## 🔧 **Configuração**

### **`gunicorn_config.py`**
```python
# Configurações principais
bind = "0.0.0.0:8080"           # Interface e porta
workers = CPU_COUNT * 2 + 1     # Workers baseados no CPU
worker_class = "sync"           # Tipo de worker
timeout = 120                   # Timeout em segundos
preload_app = True              # Pre-carrega a aplicação
```

### **Características:**
- ✅ **Multi-processo**: Usa todos os cores do CPU
- ✅ **Auto-restart**: Workers são reiniciados automaticamente
- ✅ **Logs estruturados**: Access e error logs configurados
- ✅ **Compatibilidade multi-OS**: Funciona em Linux/macOS/Windows
- ✅ **Hooks personalizados**: Funções de callback configuradas

---

## 🚀 **Como Usar**

### **Método 1: Script Consolidado build.sh**
```bash
# Ver todos os comandos disponíveis
./build.sh help

# Deploy completo (install + test + produção)
./build.sh deploy

# Apenas produção
./build.sh prod

# Desenvolvimento
./build.sh dev

# Build e teste
./build.sh build

# Parar servidores
./build.sh stop

# Verificar status
./build.sh status
```

### **Método 2: Comando Direto**
```bash
gunicorn --config gunicorn_config.py run:app
```

### **Método 3: Com parâmetros customizados**
```bash
gunicorn --bind 0.0.0.0:8080 --workers 4 run:app
```

---

## 🌐 **Acesso à Aplicação**

Após iniciar o servidor:

- **Local**: http://localhost:8080
- **Rede**: http://[SEU_IP]:8080

---

## 📊 **Configurações de Performance**

### **Workers:**
- **Fórmula**: `(CPU_CORES * 2) + 1`
- **Seu sistema**: Calculado automaticamente
- **Tipo**: `sync` (adequado para Flask)

### **Recursos:**
- **Timeout**: 120 segundos
- **Keep-alive**: 5 segundos
- **Max requests por worker**: 1000
- **Jitter**: 50 (evita restart simultâneo)

### **Logs:**
- **Access log**: stdout
- **Error log**: stderr
- **Nível**: info
- **Formato personalizado**: IP, timestamp, método, status, etc.

---

## 🔍 **Comandos Úteis**

### **Com build.sh (Recomendado):**
```bash
# Verificar status dos serviços
./build.sh status

# Parar todos os servidores
./build.sh stop
```

### **Comandos manuais:**
```bash
# Verificar processos Gunicorn
ps aux | grep gunicorn

# Parar servidor manualmente
pkill -f gunicorn
```

### **Restart Gracioso:**
```bash
kill -HUP $(pgrep -f gunicorn)
```

### **Verificar Logs:**
```bash
# Os logs aparecem no terminal onde foi iniciado
# Ou redirecionar para arquivo:
gunicorn --config gunicorn_config.py run:app > app.log 2>&1
```

---

## 🛠️ **Troubleshooting**

### **Problema: Porta em uso**
```bash
# Verificar o que está usando a porta
lsof -i :8080

# Matar processo na porta
kill -9 $(lsof -t -i:8080)
```

### **Problema: Aplicação não carrega**
```bash
# Testar configuração
gunicorn --check-config --config gunicorn_config.py run:app

# Verificar se run.py tem a variável app
python3 -c "from run import app; print('OK')"
```

### **Problema: Workers morrem**
- Verificar memória disponível
- Reduzir número de workers
- Verificar logs de erro

---

## 🐳 **Para Docker/Containerização**

### **Dockerfile exemplo:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["gunicorn", "--config", "gunicorn_config.py", "run:app"]
```

---

## 📈 **Monitoramento**

### **Métricas Importantes:**
- CPU por worker
- Memória por worker
- Tempo de resposta
- Número de conexões
- Rate de erro

### **Ferramentas Recomendadas:**
- **htop**: Monitorar processos
- **nginx**: Reverse proxy
- **prometheus**: Métricas
- **grafana**: Dashboards

---

## ⚡ **Otimizações de Produção**

### **Reverse Proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Systemd Service:**
```ini
[Unit]
Description=Email Classifier Gunicorn
After=network.target

[Service]
User=app
Group=app
WorkingDirectory=/path/to/app
ExecStart=/path/to/venv/bin/gunicorn --config gunicorn_config.py run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🔐 **Segurança**

### **Recomendações:**
- ✅ Executar com usuário não-root
- ✅ Usar reverse proxy (nginx)
- ✅ Configurar SSL/TLS
- ✅ Limitar rate de requests
- ✅ Configurar firewall
- ✅ Monitorar logs

---

## 📝 **Logs Personalizados**

### **Formato de Access Log:**
```
IP TIME "METHOD PATH" STATUS SIZE "REFERER" "USER-AGENT" DURATION
```

### **Exemplo:**
```
127.0.0.1 [28/Sep/2025:12:44:07 -0300] "GET /" 200 16854 "-" "curl/8.7.1" 11845
```

---

## ✅ **Status da Instalação**

- ✅ **Gunicorn 23.0.0** instalado
- ✅ **Configuração otimizada** criada
- ✅ **Script de produção** funcional
- ✅ **Compatibilidade multi-OS** verificada
- ✅ **Aplicação testada** e funcionando
- ✅ **Documentação completa** criada

**A aplicação está pronta para produção!** 🚀