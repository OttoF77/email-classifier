from flask import render_template
from . import main

# Cria a rota para a pagina principal do blueprint main
@main.route('/')
def index():
    return render_template('index.html')