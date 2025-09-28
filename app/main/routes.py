from flask import render_template
from . import main
from flask_login import login_required
from app.main.forms import EmailForm

# Cria a rota para a pagina principal do blueprint main
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    form = EmailForm()
    return render_template('dashboard.html', form=form)
