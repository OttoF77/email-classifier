from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria instancias das bibliotecas SQLAlchemy e Migrate
db = SQLAlchemy()
migrate = Migrate()

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
    
    return app
    

