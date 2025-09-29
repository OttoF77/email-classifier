
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from . import auth

# Cria a rota /register que terá a lógica para GET (apenas mostra o formulário de registro) e POST (valida o formulário, cria um novo objeto User, usa o método set_password e o salva no banco de dados).
@auth.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'GET':
            return "<h1>Página de Registro</h1><p>Formulário de registro funcionando!</p>"
        
        if request.method == 'POST':
            return "<h1>POST Recebido</h1><p>Dados do formulário foram enviados com sucesso!</p>"
            
    except Exception as e:
        print(f"[ERROR] Erro na rota register: {str(e)}")
        return f"<h1>Erro</h1><p>Erro na rota register: {str(e)}</p>"

# Cria a rota /login que terá lógica para GET (mostra o formulário de login) e POST (encontra o usuário pelo e-mail, usa check_password para verificar a senha e, se for válida, usa a função login_user() do Flask-Login).
@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return "<h1>Página de Login</h1><p>Formulário de login funcionando!</p>"
        
        if request.method == 'POST':
            return "<h1>POST Recebido</h1><p>Dados de login foram enviados com sucesso!</p>"
            
    except Exception as e:
        print(f"[ERROR] Erro na rota login: {str(e)}")
        return f"<h1>Erro</h1><p>Erro na rota login: {str(e)}</p>"

# Cria a rota /logout: Uma rota simples que chama a função logout_user() do Flask-Login e redireciona o usuário para a página de login ou para a landing page.
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))