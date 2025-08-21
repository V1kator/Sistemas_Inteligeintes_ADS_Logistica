import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Adiciona o diretório pai ao path para importações
sys.path.insert(0, os.path.dirname(__file__))

# Importações dos modelos e configurações
from config import config
from app.models import db

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, 
                static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                instance_relative_config=True)
    
    # Carrega configuração
    app.config.from_object(config[config_name])
    
    # Configura CORS para permitir acesso do frontend
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Inicializa extensões
    db.init_app(app)
    
    # Registra blueprints (rotas)
    register_blueprints(app)
    
    # Cria tabelas do banco de dados
    with app.app_context():
        db.create_all()
        # Executa seeds iniciais se necessário
        seed_initial_data()
    
    # Rota para servir arquivos estáticos do frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Serve arquivos do frontend Vue.js"""
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "Frontend não encontrado. Execute o build do Vue.js primeiro.", 404
    
    # Rota de health check
    @app.route('/health')
    def health_check():
        """Endpoint para verificar se a API está funcionando"""
        return {
            'status': 'ok',
            'message': 'Sistema de Códigos de Barras por CEP está funcionando',
            'version': '1.0.0'
        }
    
    return app

def register_blueprints(app):
    """Registra todos os blueprints da aplicação"""
    
    # Importa e registra as rotas da API
    from app.routes import blueprints
    
    # Registra todos os blueprints
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
        print(f"✅ Blueprint registrado: {blueprint.name} -> {url_prefix}")

def seed_initial_data():
    """Insere dados iniciais no banco de dados se necessário"""
    from app.models import CepRegiao
    
    # Verifica se já existem dados
    if CepRegiao.query.count() == 0:
        print("Banco de dados vazio. Dados iniciais serão inseridos conforme uso.")

# Cria a instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Configurações para desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Iniciando Sistema de Códigos de Barras por CEP")
    print(f"📍 Servidor rodando em: http://0.0.0.0:{port}")
    print(f"🔧 Modo debug: {debug}")
    print(f"💾 Banco de dados: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

