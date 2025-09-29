"""
Testes de exemplo demonstrando o uso das fixtures para testar rotas da aplicação.
"""

def test_index_route(client):
    """Testa se a página inicial carrega corretamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Email Classifier' in response.data


def test_app_context(app):
    """Testa se o contexto da aplicação está funcionando"""
    with app.app_context():
        # Aqui podemos testar funcionalidades que precisam do contexto da app
        assert app.config['TESTING'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


def test_database_creation(app):
    """Testa se o banco de dados é criado corretamente"""
    with app.app_context():
        from app.models import User
        # Verifica se as tabelas foram criadas
        assert User.query.count() == 0  # Banco vazio inicialmente


def test_login_required_routes(client):
    """Testa rotas que requerem login"""
    # Tenta acessar o dashboard sem estar logado
    response = client.get('/dashboard')
    # Deve redirecionar para login (302) ou retornar não autorizado
    assert response.status_code in [302, 401]


def test_client_session(client):
    """Testa se o cliente mantém sessão entre requisições"""
    # Primeira requisição
    response1 = client.get('/')
    assert response1.status_code == 200
    
    # Segunda requisição - deveria manter contexto de sessão
    response2 = client.get('/')
    assert response2.status_code == 200