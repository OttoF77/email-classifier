from flask import Blueprint

# Cria o blueprint main
main = Blueprint('main', __name__)

# Importa as rotas após criar o blueprint
from . import routes