"""
Teste básico para verificar se as fixtures estão funcionando corretamente.
"""

def test_app_fixture(app):
    """Testa se a fixture app está funcionando corretamente"""
    assert app is not None
    assert app.config['TESTING'] is True
    assert app.config['WTF_CSRF_ENABLED'] is False


def test_client_fixture(client):
    """Testa se a fixture client está funcionando corretamente"""
    assert client is not None
    
    # Testa uma requisição básica à página inicial
    response = client.get('/')
    assert response.status_code == 200


def test_runner_fixture(runner):
    """Testa se a fixture runner está funcionando corretamente"""
    assert runner is not None