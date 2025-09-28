"""
Teste completo do fluxo de autenticação: registro, login e logout.
"""
import pytest
from app.models import User
from app import db


class TestAuthenticationFlow:
    """Classe de testes para o fluxo completo de autenticação"""

    @pytest.fixture
    def user_data(self):
        """Dados de usuário para testes"""
        return {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }

    def test_complete_authentication_flow(self, client, app, user_data):
        """
        Testa o fluxo completo: registro -> login -> acesso protegido -> logout
        """
        # 1. REGISTRO - Teste de criação de novo usuário
        print("\n=== TESTANDO REGISTRO ===")
        
        # Verifica que o banco está vazio inicialmente
        with app.app_context():
            assert User.query.count() == 0
        
        # Faz POST para registro
        register_response = client.post('/register', data=user_data, follow_redirects=False)
        
        # Verifica se o registro foi bem-sucedido (redireciona para login)
        assert register_response.status_code == 302
        assert '/login' in register_response.location
        
        # Verifica se o usuário foi criado no banco
        with app.app_context():
            user = User.query.filter_by(email=user_data['email']).first()
            assert user is not None
            assert user.username == user_data['username']
            assert user.email == user_data['email']
            assert user.check_password(user_data['password'])  # Verifica hash da senha
            assert User.query.count() == 1

        # 2. LOGIN - Teste de autenticação
        print("\n=== TESTANDO LOGIN ===")
        
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        
        # Faz POST para login
        login_response = client.post('/login', data=login_data, follow_redirects=False)
        
        # Verifica se o login foi bem-sucedido (redireciona para index)
        assert login_response.status_code == 302
        assert login_response.location.endswith('/')  # Redireciona para página inicial

        # 3. ACESSO A ROTA PROTEGIDA - Teste de autorização
        print("\n=== TESTANDO ACESSO AUTENTICADO ===")
        
        # Agora que está logado, deve conseguir acessar o dashboard
        dashboard_response = client.get('/dashboard', follow_redirects=True)
        assert dashboard_response.status_code == 200
        assert b'Dashboard' in dashboard_response.data or b'dashboard' in dashboard_response.data

        # 4. LOGOUT - Teste de encerramento de sessão
        print("\n=== TESTANDO LOGOUT ===")
        
        logout_response = client.get('/logout', follow_redirects=False)
        
        # Verifica se o logout redireciona para login
        assert logout_response.status_code == 302
        assert '/login' in logout_response.location

        # 5. VERIFICAÇÃO PÓS-LOGOUT - Não deve mais ter acesso a rotas protegidas
        print("\n=== TESTANDO ACESSO APÓS LOGOUT ===")
        
        dashboard_after_logout = client.get('/dashboard', follow_redirects=False)
        # Deve ser redirecionado para login (não autenticado)
        assert dashboard_after_logout.status_code == 302

    def test_register_with_invalid_data(self, client):
        """Testa registro com dados inválidos"""
        # Teste com senhas diferentes
        invalid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'different_password'
        }
        
        response = client.post('/register', data=invalid_data)
        assert response.status_code == 200  # Retorna ao formulário
        # Como WTF_CSRF_ENABLED=False, o erro deve ser de validação de senha

    def test_register_duplicate_user(self, client, app, user_data):
        """Testa registro com email já existente"""
        # Primeiro registro (deve funcionar)
        client.post('/register', data=user_data)
        
        # Segundo registro com mesmo email (deve falhar)
        duplicate_response = client.post('/register', data=user_data)
        assert duplicate_response.status_code == 200  # Retorna ao formulário
        
        # Verifica que só existe um usuário no banco
        with app.app_context():
            assert User.query.count() == 1

    def test_login_with_wrong_credentials(self, client, app, user_data):
        """Testa login com credenciais incorretas"""
        # Primeiro cria um usuário
        client.post('/register', data=user_data)
        
        # Tenta login com senha errada
        wrong_login_data = {
            'email': user_data['email'],
            'password': 'wrong_password'
        }
        
        response = client.post('/login', data=wrong_login_data)
        assert response.status_code == 200  # Retorna ao formulário de login
        
        # Tenta login com email inexistente
        nonexistent_login_data = {
            'email': 'nonexistent@example.com',
            'password': user_data['password']
        }
        
        response = client.post('/login', data=nonexistent_login_data)
        assert response.status_code == 200  # Retorna ao formulário de login

    def test_already_authenticated_user_redirects(self, client, user_data):
        """Testa que usuário já autenticado é redirecionado"""
        # Registra e faz login
        client.post('/register', data=user_data)
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        client.post('/login', data=login_data)
        
        # Usuário já logado tentando acessar /login deve ser redirecionado
        response = client.get('/login', follow_redirects=False)
        assert response.status_code == 302
        
        # Usuário já logado tentando acessar /register deve ser redirecionado
        response = client.get('/register', follow_redirects=False)
        assert response.status_code == 302

    def test_session_persistence(self, client, user_data):
        """Testa se a sessão persiste entre requisições"""
        # Registra e faz login
        client.post('/register', data=user_data)
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        client.post('/login', data=login_data)
        
        # Faz múltiplas requisições - deve manter autenticação
        for _ in range(3):
            response = client.get('/dashboard', follow_redirects=True)
            assert response.status_code == 200

    def test_user_authentication_state(self, client, app, user_data):
        """Testa estados de autenticação do usuário"""
        with app.app_context():
            # Cria usuário manualmente para testar
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            db.session.add(user)
            db.session.commit()
            
            # Verifica propriedades do usuário
            assert user.username == user_data['username']
            assert user.email == user_data['email']
            assert user.check_password(user_data['password'])
            assert not user.check_password('wrong_password')
            assert str(user) == f"<User {user.email}>"