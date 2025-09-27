from flask import Flask

# Cria a aplicação Flask
def create_app():
    app = Flask(__name__)
    
    # Importa e registra o blueprint main
    from app.main import main
    app.register_blueprint(main)
    
    return app

