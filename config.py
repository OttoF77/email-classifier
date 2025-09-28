import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuração do PostgreSQL - apenas do .env
    database_url = os.environ.get('DATABASE_URL')
    
    # Fix para compatibilidade com SQLAlchemy 1.4+
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///fallback.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações específicas do PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }


# Cria uma Configuração Específica para Testes
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False  # Desabilita CSRF para testes
    # Configuração do método de hash para compatibilidade
    import os
    os.environ['WERKZEUG_HASH_METHOD'] = 'pbkdf2:sha256'
