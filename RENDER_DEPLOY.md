# 🚀 Deploy no Render.com - Email Classifier

## 📋 **Pré-requisitos**

1. **Conta no Render**: [render.com](https://render.com)
2. **Repositório no GitHub**: Código deve estar no GitHub
3. **PostgreSQL Database**: Banco de dados PostgreSQL (Render oferece grátis)
4. **Python 3.11+**: Especificado em `runtime.txt` e `.python-version`

---

## 🎯 **Deploy Automático via GitHub**

### **1. Conectar Repositório**
1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub: `OttoF77/email-classifier`
4. Selecione o repositório e branch `main`

### **2. Configurações do Serviço**

| Campo | Valor |
|-------|-------|
| **Name** | `email-classifier` |
| **Environment** | `Python 3` |
| **Build Command** | `./render-build.sh` |
| **Start Command** | `gunicorn --config gunicorn_config.py run:app` |
| **Plan** | `Free` (para teste) |

### **3. Variáveis de Ambiente**

Configure estas variáveis no Render Dashboard:

```env
# Essenciais
DATABASE_URL=postgresql://usuario:senha@host:porta/database
SECRET_KEY=sua-chave-secreta-super-forte-aqui

# Flask
FLASK_ENV=production
FLASK_DEBUG=false

# Opcional (Render define automaticamente)
PORT=10000
```

⚠️ **Importante**: Não inclua `PORT` - o Render define automaticamente

### **4. Banco de Dados PostgreSQL**

#### **Opção A: PostgreSQL no Render (Gratuito)**
1. No Dashboard, clique em **"New +"** → **"PostgreSQL"**
2. Nome: `email-classifier-db`
3. Plan: **Free**
4. Copie a **External Database URL** para `DATABASE_URL`

#### **Opção B: PostgreSQL Externo**
- **ElephantSQL**: postgresql://user:pass@host/db
- **Supabase**: postgresql://user:pass@host:5432/db
- **Aiven**: postgresql://user:pass@host:5432/db

---

## 🔄 **Deploy Automático**

### **Configuração com render.yaml**
O arquivo `render.yaml` está configurado para deploy automático:

```yaml
services:
  - type: web
    name: email-classifier
    env: python
    buildCommand: "./render-build.sh"
    startCommand: "gunicorn --config gunicorn_config.py run:app"
    autoDeploy: true
```

### **Deploy Manual**
Se preferir configurar manualmente no Dashboard:

1. **Build Command**: `./render-build.sh`
2. **Start Command**: `gunicorn --config gunicorn_config.py run:app`
3. **Python Version**: `3.9.6`

---

## ✅ **Processo de Build**

O script `render-build.sh` executa automaticamente:

1. ✅ **Instala dependências** (`pip install -r requirements.txt`)
2. ✅ **Verifica bibliotecas críticas** (Flask, Gunicorn, Transformers)
3. ✅ **Executa migrações** do banco de dados
4. ✅ **Testa configuração** da aplicação
5. ✅ **Valida Gunicorn** config

---

## 🌐 **URLs de Acesso**

Após o deploy:
- **Aplicação**: `https://email-classifier.onrender.com`
- **Admin Render**: Dashboard para logs e configurações

---

## 📊 **Monitoramento**

### **Logs em Tempo Real**
```bash
# No Dashboard Render
Logs → View Live Logs
```

### **Métricas**
- **CPU/Memory Usage**: Dashboard → Metrics
- **Response Times**: Logs e métricas
- **Uptime**: 99.9% no plano Free

---

## 🐛 **Troubleshooting**

### **Problemas Comuns**

#### **1. Build Failed**
```bash
# Verificar logs de build
./render-build.sh  # Testar localmente
```

#### **2. Database Connection Error**
```env
# Verificar DATABASE_URL
DATABASE_URL=postgresql://user:pass@host:5432/db
```

#### **3. Import Errors**
```bash
# Verificar requirements.txt
pip install -r requirements.txt
```

#### **4. psycopg2 Error (Python 3.13+)**
```bash
# Erro: undefined symbol: _PyInterpreterState_Get
# Solução: Usar Python 3.11 em runtime.txt
echo "python-3.11.10" > runtime.txt
```

#### **5. Port Issues**
- Render define `PORT` automaticamente
- Não definir `PORT` nas env vars

### **Comandos de Debug**
```bash
# Testar app localmente
python run.py

# Testar Gunicorn localmente  
gunicorn --config gunicorn_config.py run:app

# Verificar banco
python -c "from app import create_app; app = create_app(); print('OK')"
```

---

## 🚀 **Deploy Otimizado**

### **Performance**
- **Workers**: Auto-calculado (CPU * 2 + 1)
- **Timeout**: 120s
- **Keep-alive**: 5s
- **Preload**: True

### **Recursos**
- **Free Plan**: 512MB RAM, CPU compartilhado
- **Starter Plan**: 1GB RAM, CPU dedicado
- **Pro Plan**: Recursos escaláveis

---

## 📚 **Recursos Úteis**

- [Render Docs - Python](https://render.com/docs/python)
- [Render Docs - PostgreSQL](https://render.com/docs/databases) 
- [Flask Deploy Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)

---

## ✨ **Status do Projeto**

✅ **Pronto para Deploy no Render**
- ✅ Arquivos de configuração criados
- ✅ Script de build otimizado  
- ✅ Gunicorn configurado para produção
- ✅ Variáveis de ambiente definidas
- ✅ PostgreSQL compatível
- ✅ Auto-deploy configurado

**🎯 Basta conectar o repositório GitHub no Render Dashboard!**