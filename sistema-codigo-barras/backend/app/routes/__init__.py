"""
Módulo de rotas da API do Sistema de Códigos de Barras por CEP

Este módulo contém todas as rotas da API REST:
- Rotas de CEP (consulta e validação)
- Rotas de produtos (CRUD)
- Rotas de códigos de barras (geração e download)
- Rotas de regiões (informações)
- Rotas de estatísticas
"""

from .cep_routes import cep_bp
from .produto_routes import produto_bp
from .barcode_routes import barcode_bp
from .region_routes import region_bp
from .stats_routes import stats_bp

# Lista de blueprints para registro na aplicação
blueprints = [
    (cep_bp, '/api/cep'),
    (produto_bp, '/api/produtos'),
    (barcode_bp, '/api/codigos-barras'),
    (region_bp, '/api/regioes'),
    (stats_bp, '/api/stats')
]

__all__ = [
    'cep_bp', 'produto_bp', 'barcode_bp', 'region_bp', 'stats_bp',
    'blueprints'
]

