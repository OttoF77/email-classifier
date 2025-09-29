from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria instancias das bibliotecas SQLAlchemy e Migrate
db = SQLAlchemy()
migrate = Migrate()

# Cria a instância do LoginManager fora da função create_app.
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Cria função para receber um ID e retornar o objeto User correspondente daquele ID.
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Cria a aplicação Flask
def create_app():
    import sys
    print("🔧 [CREATE_APP] Iniciando criação da aplicação Flask", file=sys.stderr)
    
    app = Flask(__name__)
    
    # Carrega as configurações
    app.config.from_object(Config)
    print("🔧 [CREATE_APP] Configurações carregadas", file=sys.stderr)
    
    # Importa e registra o blueprint main
    from app.main import main
    app.register_blueprint(main)
    print("🔧 [CREATE_APP] Blueprint 'main' registrado", file=sys.stderr)

    # inicializa as configiurações das bibliotecas SQLAlchemy e Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models
    print("🔧 [CREATE_APP] Database inicializado", file=sys.stderr)

    # Importa e registra o blueprint auth - FORÇADO
    print("🔧 [CREATE_APP] Importando blueprint auth...", file=sys.stderr)
    try:
        from app.auth import auth
        print(f"🔧 [CREATE_APP] Blueprint auth importado: {auth.name}", file=sys.stderr)
        app.register_blueprint(auth, url_prefix='/auth')
        print("🔧 [CREATE_APP] Blueprint 'auth' registrado com prefixo /auth", file=sys.stderr)
        
        # Verifica se as rotas foram registradas
        auth_routes = [rule for rule in app.url_map.iter_rules() if 'auth' in rule.endpoint]
        print(f"🔧 [CREATE_APP] {len(auth_routes)} rotas de auth registradas", file=sys.stderr)
        for route in auth_routes:
            print(f"   📋 {route.endpoint}: {route.rule}", file=sys.stderr)
            
    except Exception as e:
        print(f"❌ [CREATE_APP ERROR] Erro ao registrar auth blueprint: {e}", file=sys.stderr)
    
    login_manager.init_app(app)
    print("🔧 [CREATE_APP] LoginManager inicializado", file=sys.stderr)
    
    # Lista final de todas as rotas
    total_routes = len(list(app.url_map.iter_rules()))
    print(f"🔧 [CREATE_APP] Aplicação criada com {total_routes} rotas totais", file=sys.stderr)
    
    return app
    

