import os
from datetime import timedelta

class Config:
    """Configuração base da aplicação"""
    
    # Configurações básicas do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sistema-codigo-barras-secret-key-2024'
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de CORS para permitir acesso do frontend
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8080', 'http://127.0.0.1:3000', 'http://127.0.0.1:8080']
    
    # Configurações de upload de arquivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    
    # Configurações de API externa para CEP
    CEP_API_URL = 'https://viacep.com.br/ws'
    CEP_API_TIMEOUT = 10
    
    # Configurações de códigos de barras
    BARCODE_FORMAT = 'CODE128'
    BARCODE_WIDTH = 2
    BARCODE_HEIGHT = 100
    
    # Mapeamento de regiões por estado
    REGIOES_BRASIL = {
        # Norte - Identificador 1
        'AC': 1, 'AP': 1, 'AM': 1, 'PA': 1, 'RO': 1, 'RR': 1, 'TO': 1,
        # Nordeste - Identificador 1  
        'AL': 1, 'BA': 1, 'CE': 1, 'MA': 1, 'PB': 1, 'PE': 1, 'PI': 1, 'RN': 1, 'SE': 1,
        # Centro-Oeste - Identificador 2
        'DF': 2, 'GO': 2, 'MT': 2, 'MS': 2,
        # Sudeste - Identificador 3
        'ES': 3, 'MG': 3, 'RJ': 3, 'SP': 3,
        # Sul - Identificador 3
        'PR': 3, 'RS': 3, 'SC': 3
    }

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configuração para testes"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

