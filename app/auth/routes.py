
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from flask_wtf.csrf import CSRFError
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from . import auth

# Cria a rota /register que terá a lógica para GET (apenas mostra o formulário de registro) e POST (valida o formulário, cria um novo objeto User, usa o método set_password e o salva no banco de dados).
@auth.route('/register', methods=['GET', 'POST'])
def register():
    try:
        # Se usuário já está logado, redireciona para index
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        
        form = RegistrationForm()
        
        print(f"[DEBUG] Formulário de registro submetido: {form.data}")
        
        if form.validate_on_submit():
            print("[DEBUG] Formulário validado com sucesso")
            # Verifica se usuário já existe
            existing_user = User.query.filter(
                (User.email == form.email.data) | (User.username == form.username.data)
            ).first()
            
            if existing_user:
                print(f"[DEBUG] Usuário já existe: email={existing_user.email}, username={existing_user.username}")
                if existing_user.email == form.email.data:
                    flash('Este email já está cadastrado.', 'danger')
                else:
                    flash('Este nome de usuário já está em uso.', 'danger')
                return render_template('auth/register.html', form=form)
            
            # Cria novo usuário
            print(f"[DEBUG] Criando novo usuário: {form.username.data}, {form.email.data}")
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            print(f"[DEBUG] Usuário criado com ID: {user.id}")
            
            flash('Conta criada com sucesso! Você pode fazer login agora.', 'success')
            return redirect(url_for('auth.login'))
        else:
            print(f"[DEBUG] Formulário não validado. Erros: {form.errors}")
        
        return render_template('auth/register.html', form=form)
        
    except Exception as e:
        print(f"[ERROR] Erro na rota register: {str(e)}")
        db.session.rollback()
        flash('Erro interno do servidor. Tente novamente.', 'danger')
        form = RegistrationForm()
        return render_template('auth/register.html', form=form)

# Cria a rota /login que terá lógica para GET (mostra o formulário de login) e POST (encontra o usuário pelo e-mail, usa check_password para verificar a senha e, se for válida, usa a função login_user() do Flask-Login).
@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        # Se usuário já está logado, redireciona para index
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                
                # Redireciona para página solicitada ou index
                next_page = request.args.get('next')
                if not next_page or url_for('main.index') not in next_page:
                    next_page = url_for('main.index')
                
                flash(f'Bem-vindo, {user.username}!', 'success')
                return redirect(next_page)
            else:
                flash('Email ou senha inválidos.', 'danger')
        
        return render_template('auth/login.html', form=form)
        
    except Exception as e:
        print(f"[ERROR] Erro na rota login: {str(e)}")
        flash('Erro interno do servidor. Tente novamente.', 'danger')
        form = LoginForm()
        return render_template('auth/login.html', form=form)

# Cria a rota /logout: Uma rota simples que chama a função logout_user() do Flask-Login e redireciona o usuário para a página de login ou para a landing page.
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Handler para erros CSRF
@auth.errorhandler(CSRFError)
def handle_csrf_error(e):
    print(f"[ERROR] CSRF Error: {str(e)}")
    flash('Token de segurança inválido. Por favor, tente novamente.', 'danger')
    return redirect(request.url)