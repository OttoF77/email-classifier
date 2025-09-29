
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from . import auth

# Cria a rota /register que terá a lógica para GET (apenas mostra o formulário de registro) e POST (valida o formulário, cria um novo objeto User, usa o método set_password e o salva no banco de dados).
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registro realizado com sucesso!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

# Cria a rota /login que terá lógica para GET (mostra o formulário de login) e POST (encontra o usuário pelo e-mail, usa check_password para verificar a senha e, se for válida, usa a função login_user() do Flask-Login).
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(f"[DEBUG] Tentativa de login com email: {form.email.data}")
        user = User.query.filter_by(email=form.email.data).first()
        print(f"[DEBUG] Usuário encontrado: {user is not None}")
        if user:
            print(f"[DEBUG] Hash armazenado: {user.password_hash[:20]}...")
            password_check = user.check_password(form.password.data)
            print(f"[DEBUG] Verificação de senha: {password_check}")
            if password_check:
                login_user(user)
                flash('Login realizado com sucesso!')
                print(f"[DEBUG] Login bem-sucedido para usuário: {user.email}")
                return redirect(url_for('main.index'))
        print(f"[DEBUG] Falha no login - usuário ou senha incorretos")
        flash('Email ou senha inválidos.')
    else:
        if request.method == 'POST':
            print(f"[DEBUG] Formulário não passou na validação: {form.errors}")
    return render_template('auth/login.html', title='Login', form=form)

# Cria a rota /logout: Uma rota simples que chama a função logout_user() do Flask-Login e redireciona o usuário para a página de login ou para a landing page.
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))