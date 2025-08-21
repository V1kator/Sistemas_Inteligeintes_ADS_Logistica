"""
Rotas da API para estatísticas gerais do sistema
"""

from flask import Blueprint, jsonify
from app.models import db, Produto, CodigoBarras, CepRegiao
from app.services import BarcodeService, RegionService, CepService
from app.utils import create_success_response, create_error_response
from app.utils.constants import HTTP_STATUS, ERROR_MESSAGES
from sqlalchemy import func

# Cria blueprint para rotas de estatísticas
stats_bp = Blueprint('stats', __name__)

# Instancia serviços
barcode_service = BarcodeService()
region_service = RegionService()
cep_service = CepService()

@stats_bp.route('/', methods=['GET'])
def estatisticas_gerais():
    """
    Retorna estatísticas gerais do sistema
    
    Returns:
        JSON: Estatísticas completas do sistema
    """
    try:
        # Estatísticas de produtos
        total_produtos = Produto.query.filter_by(ativo=True).count()
        
        # Estatísticas de códigos de barras
        total_codigos = CodigoBarras.query.filter_by(ativo=True).count()
        total_downloads = db.session.query(
            func.sum(CodigoBarras.total_downloads)
        ).filter_by(ativo=True).scalar() or 0
        
        # Estatísticas de CEPs
        total_ceps_cache = CepRegiao.query.count()
        
        # Estatísticas por região
        stats_produtos_regiao = db.session.query(
            Produto.regiao_id,
            func.count(Produto.id).label('total_produtos')
        ).filter_by(ativo=True).group_by(Produto.regiao_id).all()
        
        stats_codigos_regiao = db.session.query(
            CodigoBarras.regiao_identificador,
            func.count(CodigoBarras.id).label('total_codigos'),
            func.sum(CodigoBarras.total_downloads).label('total_downloads')
        ).filter_by(ativo=True).group_by(CodigoBarras.regiao_identificador).all()
        
        # Formata estatísticas por região
        regioes_stats = {}
        for regiao_id in [1, 2, 3]:
            nome_regiao = region_service.get_nome_regiao(regiao_id)
            
            # Produtos por região
            produtos_regiao = next(
                (stat.total_produtos for stat in stats_produtos_regiao if stat.regiao_id == regiao_id),
                0
            )
            
            # Códigos por região
            codigos_stat = next(
                (stat for stat in stats_codigos_regiao if stat.regiao_identificador == regiao_id),
                None
            )
            
            codigos_regiao = codigos_stat.total_codigos if codigos_stat else 0
            downloads_regiao = codigos_stat.total_downloads if codigos_stat and codigos_stat.total_downloads else 0
            
            regioes_stats[regiao_id] = {
                'nome': nome_regiao,
                'total_produtos': produtos_regiao,
                'total_codigos': codigos_regiao,
                'total_downloads': downloads_regiao
            }
        
        # Estatísticas de uso recente (últimos 30 dias)
        from datetime import datetime, timedelta
        data_limite = datetime.now() - timedelta(days=30)
        
        produtos_recentes = Produto.query.filter(
            Produto.ativo == True,
            Produto.data_criacao >= data_limite
        ).count()
        
        codigos_recentes = CodigoBarras.query.filter(
            CodigoBarras.ativo == True,
            CodigoBarras.data_criacao >= data_limite
        ).count()
        
        resultado = {
            'resumo_geral': {
                'total_produtos': total_produtos,
                'total_codigos_barras': total_codigos,
                'total_downloads': total_downloads,
                'total_ceps_cache': total_ceps_cache
            },
            'estatisticas_por_regiao': regioes_stats,
            'atividade_recente': {
                'produtos_ultimos_30_dias': produtos_recentes,
                'codigos_ultimos_30_dias': codigos_recentes,
                'periodo': '30 dias'
            },
            'data_atualizacao': datetime.now().isoformat()
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message="Estatísticas gerais obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@stats_bp.route('/produtos', methods=['GET'])
def estatisticas_produtos():
    """
    Retorna estatísticas específicas de produtos
    
    Returns:
        JSON: Estatísticas de produtos
    """
    try:
        # Total de produtos
        total_produtos = Produto.query.filter_by(ativo=True).count()
        
        # Produtos por região
        stats_regiao = db.session.query(
            Produto.regiao_id,
            func.count(Produto.id).label('total')
        ).filter_by(ativo=True).group_by(Produto.regiao_id).all()
        
        # Produtos por estado
        stats_estado = db.session.query(
            Produto.estado,
            func.count(Produto.id).label('total')
        ).filter_by(ativo=True).group_by(Produto.estado).order_by(func.count(Produto.id).desc()).all()
        
        # Formata estatísticas
        produtos_por_regiao = {}
        for stat in stats_regiao:
            regiao_id = stat.regiao_id
            produtos_por_regiao[regiao_id] = {
                'nome': region_service.get_nome_regiao(regiao_id),
                'total_produtos': stat.total
            }
        
        produtos_por_estado = [
            {
                'estado': stat.estado,
                'total_produtos': stat.total,
                'regiao_id': region_service.get_regiao_por_estado(stat.estado),
                'regiao_nome': region_service.get_nome_regiao(
                    region_service.get_regiao_por_estado(stat.estado)
                )
            }
            for stat in stats_estado
        ]
        
        resultado = {
            'total_produtos': total_produtos,
            'produtos_por_regiao': produtos_por_regiao,
            'produtos_por_estado': produtos_por_estado,
            'top_5_estados': produtos_por_estado[:5]
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message="Estatísticas de produtos obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@stats_bp.route('/codigos-barras', methods=['GET'])
def estatisticas_codigos_barras():
    """
    Retorna estatísticas específicas de códigos de barras
    
    Returns:
        JSON: Estatísticas de códigos de barras
    """
    try:
        stats = barcode_service.get_estatisticas()
        
        return jsonify(create_success_response(
            data=stats,
            message="Estatísticas de códigos de barras obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@stats_bp.route('/cep', methods=['GET'])
def estatisticas_cep():
    """
    Retorna estatísticas do cache de CEPs
    
    Returns:
        JSON: Estatísticas do cache de CEPs
    """
    try:
        stats = cep_service.get_estatisticas_cache()
        
        return jsonify(create_success_response(
            data=stats,
            message="Estatísticas de CEP obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@stats_bp.route('/regioes', methods=['GET'])
def estatisticas_regioes():
    """
    Retorna estatísticas das regiões
    
    Returns:
        JSON: Estatísticas das regiões
    """
    try:
        stats = region_service.get_estatisticas_regioes()
        
        return jsonify(create_success_response(
            data=stats,
            message="Estatísticas de regiões obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@stats_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Retorna dados resumidos para dashboard
    
    Returns:
        JSON: Dados do dashboard
    """
    try:
        # Contadores principais
        total_produtos = Produto.query.filter_by(ativo=True).count()
        total_codigos = CodigoBarras.query.filter_by(ativo=True).count()
        total_downloads = db.session.query(
            func.sum(CodigoBarras.total_downloads)
        ).filter_by(ativo=True).scalar() or 0
        
        # Atividade recente (últimos 7 dias)
        from datetime import datetime, timedelta
        data_limite = datetime.now() - timedelta(days=7)
        
        produtos_semana = Produto.query.filter(
            Produto.ativo == True,
            Produto.data_criacao >= data_limite
        ).count()
        
        codigos_semana = CodigoBarras.query.filter(
            CodigoBarras.ativo == True,
            CodigoBarras.data_criacao >= data_limite
        ).count()
        
        # Top 3 regiões por códigos de barras
        top_regioes = db.session.query(
            CodigoBarras.regiao_identificador,
            func.count(CodigoBarras.id).label('total')
        ).filter_by(ativo=True).group_by(
            CodigoBarras.regiao_identificador
        ).order_by(func.count(CodigoBarras.id).desc()).limit(3).all()
        
        top_regioes_formatado = [
            {
                'regiao_id': stat.regiao_identificador,
                'nome': region_service.get_nome_regiao(stat.regiao_identificador),
                'total_codigos': stat.total
            }
            for stat in top_regioes
        ]
        
        resultado = {
            'contadores': {
                'produtos': total_produtos,
                'codigos_barras': total_codigos,
                'downloads': total_downloads
            },
            'atividade_semanal': {
                'novos_produtos': produtos_semana,
                'novos_codigos': codigos_semana
            },
            'top_regioes': top_regioes_formatado,
            'data_atualizacao': datetime.now().isoformat()
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message="Dados do dashboard obtidos com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@stats_bp.route('/sistema', methods=['GET'])
def info_sistema():
    """
    Retorna informações do sistema
    
    Returns:
        JSON: Informações do sistema
    """
    try:
        from app.utils.constants import API_CONFIG
        from datetime import datetime
        import os
        
        # Informações do banco de dados
        db_path = os.path.join(os.path.dirname(__file__), '../../database/app.db')
        db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        
        # Informações da aplicação
        resultado = {
            'aplicacao': {
                'nome': 'Sistema de Códigos de Barras por CEP',
                'versao': API_CONFIG['versao'],
                'ambiente': 'desenvolvimento'
            },
            'banco_dados': {
                'tipo': 'SQLite',
                'tamanho_bytes': db_size,
                'tamanho_formatado': f"{db_size / 1024:.1f} KB" if db_size > 0 else "0 KB"
            },
            'configuracoes': {
                'timeout_api': API_CONFIG['timeout_padrao'],
                'limite_requisicoes': API_CONFIG['limite_requisicoes_por_minuto'],
                'tamanho_pagina_padrao': API_CONFIG['tamanho_pagina_padrao']
            },
            'data_consulta': datetime.now().isoformat()
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message="Informações do sistema obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

# Rota de teste
@stats_bp.route('/teste', methods=['GET'])
def teste_stats():
    """
    Rota de teste para o blueprint de estatísticas
    
    Returns:
        JSON: Mensagem de teste
    """
    return jsonify(create_success_response(
        data={'blueprint': 'stats', 'status': 'funcionando'},
        message="Blueprint de estatísticas está funcionando corretamente"
    )), HTTP_STATUS['OK']

