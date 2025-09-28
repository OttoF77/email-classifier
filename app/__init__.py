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
    app = Flask(__name__)
    
    # Carrega as configurações
    app.config.from_object(Config)
    
    # Importa e registra o blueprint main
    from app.main import main
    app.register_blueprint(main)

    # inicializa as configiurações das bibliotecas SQLAlchemy e Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    # Importa e registra o blueprint auth
    from app.auth import auth
    app.register_blueprint(auth)
    login_manager.init_app(app)
    
    return app
    

