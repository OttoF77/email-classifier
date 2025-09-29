import pytest
import os
import tempfile
from app import create_app, db
from config import TestConfig

# Configurar método de hash compatível para testes
os.environ['WERKZEUG_HASH_METHOD'] = 'pbkdf2:sha256'


@pytest.fixture
def app():
    """
    Fixture que cria e configura uma instância da aplicação Flask para testes.
    
    Returns:
        Flask: Instância da aplicação configurada para testes
    """
    # Cria a aplicação com configuração de teste
    app = create_app()
    app.config.from_object(TestConfig)
    
    # Cria um contexto de aplicação para os testes
    with app.app_context():
        # Cria todas as tabelas do banco de dados
        db.create_all()
        
        yield app
        
        # Limpa o banco após os testes
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Fixture que cria um cliente de teste para simular requisições HTTP.
    
    Args:
        app: Fixture da aplicação Flask
        
    Returns:
        FlaskClient: Cliente de teste para fazer requisições
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Fixture que cria um runner para executar comandos CLI da aplicação.
    
    Args:
        app: Fixture da aplicação Flask
        
    Returns:
        FlaskCliRunner: Runner para comandos CLI
    """
    return app.test_cli_runner()
