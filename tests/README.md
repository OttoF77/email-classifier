# Guia de Fixtures de Teste

Este documento explica como usar as fixtures configuradas no arquivo `tests/conftest.py` para testar a aplicação Email Classifier.

## Fixtures Disponíveis

### 1. `app` - Fixture da Aplicação Flask

**Descrição**: Cria uma instância da aplicação Flask configurada especificamente para testes.

**Configurações de Teste**:
- `TESTING = True`: Ativa o modo de teste
- `WTF_CSRF_ENABLED = False`: Desabilita CSRF para facilitar os testes
- `SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'`: Usa banco SQLite em memória
- `SECRET_KEY = 'test-secret-key'`: Chave secreta para testes

**Uso**:
```python
def test_app_configuration(app):
    assert app.config['TESTING'] is True
    assert app.config['WTF_CSRF_ENABLED'] is False
```

### 2. `client` - Fixture do Cliente de Teste

**Descrição**: Fornece um cliente de teste que simula requisições HTTP para a aplicação, como se fosse um navegador.

**Funcionalidades**:
- Fazer requisições GET, POST, PUT, DELETE
- Simular envio de formulários
- Testar autenticação e sessões
- Verificar códigos de status e conteúdo das respostas

**Uso**:
```python
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Email Classifier' in response.data
```

### 3. `runner` - Fixture do CLI Runner

**Descrição**: Permite testar comandos CLI da aplicação Flask.

**Uso**:
```python
def test_cli_command(runner):
    result = runner.invoke(args=['--help'])
    assert result.exit_code == 0
```

## Exemplos de Uso

### Testando Rotas

```python
def test_login_page(client):
    """Testa se a página de login carrega corretamente"""
    response = client.get('/login')
    assert response.status_code == 200

def test_protected_route(client):
    """Testa rota que requer autenticação"""
    response = client.get('/dashboard')
    # Deve redirecionar para login
    assert response.status_code == 302
```

### Testando com Banco de Dados

```python
def test_user_creation(app):
    """Testa criação de usuário no banco"""
    with app.app_context():
        from app.models import User
        from app import db
        
        user = User(username='test', email='test@test.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        assert User.query.count() == 1
```

### Testando Formulários

```python
def test_form_submission(client):
    """Testa envio de formulário"""
    response = client.post('/classify', data={
        'content': 'Teste de email',
        'csrf_token': 'disabled'  # CSRF desabilitado nos testes
    })
    assert response.status_code in [200, 302]
```

## Vantagens das Fixtures

1. **Isolamento**: Cada teste roda em um ambiente limpo
2. **Reutilização**: As fixtures podem ser usadas em múltiplos testes
3. **Configuração Automática**: Setup e teardown automáticos
4. **Banco em Memória**: Testes rápidos sem afetar dados reais
5. **Fácil Debugging**: Configuração específica para testes

## Executando os Testes

```bash
# Todos os testes
python3 -m pytest tests/ -v

# Teste específico
python3 -m pytest tests/test_routes.py -v

# Com coverage
python3 -m pytest tests/ --cov=app
```