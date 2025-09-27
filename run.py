from app import create_app

# Configura o run.py para carregar e executar a aplicação Flask.
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)