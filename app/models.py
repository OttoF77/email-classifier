from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Cria User: colunas id (chave primária), usuário (não nulo), email (não nulo) e password_hash (não nulo)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    def __repr__(self):
        return f'<User {self.email}>'
    
    # Cria o método set_password(self, password) que recebe uma senha, gera um hash seguro e o armazena no campo password_hash.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Cria o método check_password(self, password) que recebe uma senha e a compara com o hash armazenado, retornando True ou False.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Cria EmailClassification: colunas como id (chave primária), content (o texto do email), category (a classificação "Produtivo"/"Improdutivo"), suggested_response (a resposta da IA) e user_id (foreign key).
class EmailClassification(db.Model):
    __tablename__ = 'email_classifications'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    suggested_response = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('email_classifications', lazy=True))
    def __repr__(self):
        return f'<EmailClassification {self.category} for User ID {self.user_id}>'
    
