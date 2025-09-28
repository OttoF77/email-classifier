"""
Teste da funcionalidade principal de classificação de emails.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.models import User, EmailClassification
from app import db
import io


class TestEmailClassification:
    """Classe de testes para funcionalidade de classificação de emails"""

    @pytest.fixture
    def authenticated_user(self, client, app):
        """Fixture que cria e autentica um usuário"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        
        # Registra o usuário
        client.post('/register', data=user_data)
        
        # Faz login
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        client.post('/login', data=login_data)
        
        # Retorna dados do usuário para uso nos testes
        with app.app_context():
            user = User.query.filter_by(email=user_data['email']).first()
            return user

    @patch('app.main.routes.classify_email')
    @patch('app.main.routes.generate_response')
    def test_email_classification_text_content(self, mock_generate_response, mock_classify_email, 
                                             client, app, authenticated_user):
        """
        Testa classificação de email usando conteúdo de texto
        """
        # Mock das funções de IA
        mock_classify_email.return_value = "Produtivo"
        mock_generate_response.return_value = "Obrigado pelo seu email. Vamos analisar sua proposta e retornar em breve."
        
        email_content = "Olá, gostaria de discutir uma oportunidade de negócio interessante que pode ser muito lucrativa para ambas as partes."
        
        # Verifica estado inicial do banco
        with app.app_context():
            initial_count = EmailClassification.query.count()
            assert initial_count == 0
        
        # Envia formulário com conteúdo de texto
        form_data = {
            'content': email_content,
            'submit': 'Classificar Email'
        }
        
        response = client.post('/dashboard', data=form_data, follow_redirects=True)
        
        # Verifica se a resposta foi bem-sucedida
        assert response.status_code == 200
        assert b'E-mail classificado com sucesso!' in response.data
        
        # Verifica se as funções de IA foram chamadas
        mock_classify_email.assert_called_once_with(email_content)
        mock_generate_response.assert_called_once_with(email_content)
        
        # Verifica se o registro foi criado no banco
        with app.app_context():
            classifications = EmailClassification.query.all()
            assert len(classifications) == 1
            
            classification = classifications[0]
            assert classification.content == email_content
            assert classification.category == "Produtivo"
            assert classification.suggested_response == "Obrigado pelo seu email. Vamos analisar sua proposta e retornar em breve."
            assert classification.user_id == authenticated_user.id
            assert classification.timestamp is not None

    @patch('app.main.routes.classify_email')
    @patch('app.main.routes.generate_response')
    def test_email_classification_txt_file(self, mock_generate_response, mock_classify_email,
                                         client, app, authenticated_user):
        """
        Testa classificação de email usando arquivo .txt
        """
        # Mock das funções de IA
        mock_classify_email.return_value = "Improdutivo"
        mock_generate_response.return_value = "Obrigado pelo contato. Não temos interesse neste tipo de proposta no momento."
        
        email_content = "PROMOÇÃO IMPERDÍVEL! Ganhe dinheiro fácil trabalhando de casa! Clique aqui!"
        
        # Cria arquivo .txt em memória
        txt_file = io.BytesIO(email_content.encode('utf-8'))
        
        # Envia formulário com arquivo
        form_data = {
            'file': (txt_file, 'email_spam.txt', 'text/plain'),
            'submit': 'Classificar Email'
        }
        
        response = client.post('/dashboard', data=form_data, 
                             follow_redirects=True, content_type='multipart/form-data')
        
        # Verifica se a resposta foi bem-sucedida
        assert response.status_code == 200
        assert b'E-mail classificado com sucesso!' in response.data
        
        # Verifica se as funções de IA foram chamadas
        mock_classify_email.assert_called_once_with(email_content)
        mock_generate_response.assert_called_once_with(email_content)
        
        # Verifica se o registro foi criado no banco
        with app.app_context():
            classification = EmailClassification.query.first()
            assert classification.content == email_content
            assert classification.category == "Improdutivo"
            assert classification.user_id == authenticated_user.id

    def test_email_classification_empty_content(self, client, authenticated_user):
        """
        Testa comportamento com conteúdo vazio
        """
        # Envia formulário sem conteúdo
        form_data = {
            'content': '',
            'submit': 'Classificar Email'
        }
        
        response = client.post('/dashboard', data=form_data, follow_redirects=True)
        
        # Verifica se retorna erro apropriado
        assert response.status_code == 200
        assert b'Nenhum conte' in response.data or b'deve inserir' in response.data

    @patch('app.main.routes.classify_email')
    @patch('app.main.routes.generate_response')
    def test_multiple_classifications_same_user(self, mock_generate_response, mock_classify_email,
                                              client, app, authenticated_user):
        """
        Testa múltiplas classificações pelo mesmo usuário
        """
        # Mock das funções de IA
        mock_classify_email.side_effect = ["Produtivo", "Improdutivo"]
        mock_generate_response.side_effect = [
            "Resposta para email produtivo",
            "Resposta para email improdutivo"
        ]
        
        # Primeira classificação
        form_data1 = {
            'content': 'Email produtivo sobre reunião de trabalho',
            'submit': 'Classificar Email'
        }
        client.post('/dashboard', data=form_data1, follow_redirects=True)
        
        # Segunda classificação
        form_data2 = {
            'content': 'Email de spam com promoções',
            'submit': 'Classificar Email'
        }
        client.post('/dashboard', data=form_data2, follow_redirects=True)
        
        # Verifica se ambas foram criadas
        with app.app_context():
            classifications = EmailClassification.query.filter_by(user_id=authenticated_user.id).all()
            assert len(classifications) == 2
            
            # Verifica se são diferentes
            categories = [c.category for c in classifications]
            assert "Produtivo" in categories
            assert "Improdutivo" in categories

    @patch('app.main.routes.classify_email')
    @patch('app.main.routes.generate_response')
    def test_classification_user_isolation(self, mock_generate_response, mock_classify_email,
                                         client, app):
        """
        Testa que classificações são isoladas por usuário
        """
        # Mock das funções de IA
        mock_classify_email.return_value = "Produtivo"
        mock_generate_response.return_value = "Resposta padrão"
        
        # Cria primeiro usuário
        user1_data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        client.post('/register', data=user1_data)
        client.post('/login', data={'email': user1_data['email'], 'password': user1_data['password']})
        
        # Faz classificação com user1
        client.post('/dashboard', data={
            'content': 'Email do usuário 1',
            'submit': 'Classificar Email'
        })
        
        # Logout do user1
        client.get('/logout')
        
        # Cria segundo usuário
        user2_data = {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        client.post('/register', data=user2_data)
        client.post('/login', data={'email': user2_data['email'], 'password': user2_data['password']})
        
        # Faz classificação com user2
        client.post('/dashboard', data={
            'content': 'Email do usuário 2',
            'submit': 'Classificar Email'
        })
        
        # Verifica isolamento
        with app.app_context():
            user1 = User.query.filter_by(email=user1_data['email']).first()
            user2 = User.query.filter_by(email=user2_data['email']).first()
            
            user1_classifications = EmailClassification.query.filter_by(user_id=user1.id).all()
            user2_classifications = EmailClassification.query.filter_by(user_id=user2.id).all()
            
            assert len(user1_classifications) == 1
            assert len(user2_classifications) == 1
            assert user1_classifications[0].content == 'Email do usuário 1'
            assert user2_classifications[0].content == 'Email do usuário 2'

    @patch('app.main.routes.classify_email')
    @patch('app.main.routes.generate_response')
    def test_ai_service_error_handling(self, mock_generate_response, mock_classify_email,
                                     client, authenticated_user):
        """
        Testa tratamento de erros do serviço de IA
        """
        # Mock para simular erro no serviço de IA
        mock_classify_email.side_effect = Exception("Erro no modelo de IA")
        
        form_data = {
            'content': 'Email para testar erro',
            'submit': 'Classificar Email'
        }
        
        response = client.post('/dashboard', data=form_data, follow_redirects=True)
        
        # Verifica se o erro foi tratado adequadamente
        assert response.status_code == 200
        assert b'Erro ao processar com IA' in response.data

    def test_unauthorized_access_to_dashboard(self, client):
        """
        Testa que usuários não autenticados não podem acessar o dashboard
        """
        response = client.post('/dashboard', data={
            'content': 'Tentativa de acesso não autorizado',
            'submit': 'Classificar Email'
        }, follow_redirects=False)
        
        # Deve redirecionar para login
        assert response.status_code == 302
        assert '/login' in response.location

    @patch('app.main.routes.classify_email')
    @patch('app.main.routes.generate_response')
    def test_dashboard_displays_user_classifications(self, mock_generate_response, mock_classify_email,
                                                   client, app, authenticated_user):
        """
        Testa que o dashboard exibe as classificações do usuário
        """
        # Mock das funções de IA
        mock_classify_email.return_value = "Produtivo"
        mock_generate_response.return_value = "Resposta de teste"
        
        # Cria uma classificação
        form_data = {
            'content': 'Email de teste para visualização',
            'submit': 'Classificar Email'
        }
        client.post('/dashboard', data=form_data)
        
        # Acessa o dashboard
        response = client.get('/dashboard')
        
        # Verifica se a classificação aparece na página
        assert response.status_code == 200
        assert b'Email de teste para visualiza' in response.data
        assert b'Produtivo' in response.data