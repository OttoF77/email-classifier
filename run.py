import os
import sys
from app import create_app

# Debug imediato no carregamento
print("🚀 [STARTUP] Iniciando criação da aplicação...", file=sys.stderr)

# Cria a instância da aplicação Flask
app = create_app()

# Força o registro das rotas de auth imediatamente
with app.app_context():
    print(f"🚀 [STARTUP] Aplicação criada com {len(list(app.url_map.iter_rules()))} rotas", file=sys.stderr)
    
    # Lista todas as rotas para debug
    auth_routes = []
    all_routes = []
    for rule in app.url_map.iter_rules():
        route_info = f"{rule.endpoint}: {rule.rule}"
        all_routes.append(route_info)
        if 'auth' in rule.endpoint:
            auth_routes.append(route_info)
            print(f"📋 [AUTH ROUTE FOUND] {route_info}", file=sys.stderr)
    
    if not auth_routes:
        print("❌ [ERROR] Nenhuma rota de autenticação encontrada!", file=sys.stderr)
        print("📋 [ALL ROUTES]", file=sys.stderr)
        for route in all_routes[:10]:  # Primeiras 10 rotas
            print(f"   {route}", file=sys.stderr)
    else:
        print(f"✅ [SUCCESS] {len(auth_routes)} rotas de autenticação registradas", file=sys.stderr)

# Debug: Adiciona endpoint para verificar rotas registradas
@app.route('/debug/routes')
def debug_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        url = urllib.parse.unquote(rule.rule)
        output.append(f"{rule.endpoint}: {methods} {url}")
    return '<br>'.join(sorted(output))

# Teste direto das rotas de auth
@app.route('/test/auth')
def test_auth():
    try:
        from app.auth.routes import auth
        return f"Auth blueprint importado: {auth.name}"
    except Exception as e:
        return f"Erro ao importar auth: {str(e)}"

# Configura o run.py para carregar e executar a aplicação Flask.
if __name__ == '__main__':
    app.run(debug=True)