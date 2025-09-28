from app import create_app

# Cria a instância da aplicação Flask
app = create_app()

# Configura o run.py para carregar e executar a aplicação Flask.
if __name__ == '__main__':
    app.run(debug=True)