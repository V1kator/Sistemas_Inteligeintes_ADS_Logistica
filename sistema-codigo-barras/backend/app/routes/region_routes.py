"""
Rotas da API para informações sobre regiões brasileiras
"""

from flask import Blueprint, request, jsonify
from app.services import RegionService
from app.utils import create_success_response, create_error_response
from app.utils.constants import HTTP_STATUS, ERROR_MESSAGES

# Cria blueprint para rotas de regiões
region_bp = Blueprint('region', __name__)

# Instancia serviços
region_service = RegionService()

@region_bp.route('/', methods=['GET'])
def listar_regioes():
    """
    Lista todas as regiões com suas informações
    
    Returns:
        JSON: Lista de todas as regiões
    """
    try:
        regioes = region_service.get_todas_regioes()
        
        return jsonify(create_success_response(
            data={
                'regioes': regioes,
                'total_regioes': len(regioes)
            },
            message=f"{len(regioes)} região(ões) encontrada(s)"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/<int:regiao_id>', methods=['GET'])
def obter_regiao(regiao_id):
    """
    Obtém informações detalhadas de uma região específica
    
    Args:
        regiao_id (int): ID da região (1, 2 ou 3)
        
    Returns:
        JSON: Dados detalhados da região ou erro
    """
    try:
        if regiao_id not in [1, 2, 3]:
            return jsonify(create_error_response(
                message="ID da região deve ser 1, 2 ou 3",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        regiao = region_service.get_regiao_detalhada(regiao_id)
        
        if not regiao:
            return jsonify(create_error_response(
                message="Região não encontrada",
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        return jsonify(create_success_response(
            data=regiao,
            message="Região encontrada com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/estado/<uf>', methods=['GET'])
def obter_regiao_por_estado(uf):
    """
    Obtém região de um estado específico
    
    Args:
        uf (str): Sigla do estado (UF)
        
    Returns:
        JSON: Dados da região do estado ou erro
    """
    try:
        uf_upper = uf.upper().strip()
        
        # Valida se é um estado brasileiro válido
        if not region_service.validar_estado(uf_upper):
            return jsonify(create_error_response(
                message="Estado (UF) inválido",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        regiao_id = region_service.get_regiao_por_estado(uf_upper)
        regiao = region_service.get_regiao_detalhada(regiao_id)
        
        resultado = {
            'estado': uf_upper,
            'regiao': regiao
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"Estado {uf_upper} pertence à região {regiao['nome']}"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/estados/<int:regiao_id>', methods=['GET'])
def listar_estados_regiao(regiao_id):
    """
    Lista todos os estados de uma região
    
    Args:
        regiao_id (int): ID da região (1, 2 ou 3)
        
    Returns:
        JSON: Lista de estados da região ou erro
    """
    try:
        if regiao_id not in [1, 2, 3]:
            return jsonify(create_error_response(
                message="ID da região deve ser 1, 2 ou 3",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        estados = region_service.get_estados_por_regiao(regiao_id)
        nome_regiao = region_service.get_nome_regiao(regiao_id)
        
        resultado = {
            'regiao_id': regiao_id,
            'nome_regiao': nome_regiao,
            'estados': estados,
            'total_estados': len(estados)
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"{len(estados)} estado(s) encontrado(s) na região {nome_regiao}"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/buscar', methods=['GET'])
def buscar_regiao():
    """
    Busca região por nome ou palavra-chave
    
    Query Parameters:
        q (str): Termo de busca
        
    Returns:
        JSON: Região encontrada ou erro
    """
    try:
        termo = request.args.get('q', '').strip()
        
        if not termo:
            return jsonify(create_error_response(
                message="Termo de busca é obrigatório",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        regiao = region_service.buscar_regiao_por_nome(termo)
        
        if not regiao:
            return jsonify(create_error_response(
                message=f"Nenhuma região encontrada para '{termo}'",
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        resultado = {
            'termo_busca': termo,
            'regiao': regiao
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"Região encontrada para '{termo}'"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/stats', methods=['GET'])
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
            message="Estatísticas das regiões obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/mapeamento', methods=['GET'])
def mapeamento_completo():
    """
    Retorna mapeamento completo de estados por região
    
    Returns:
        JSON: Mapeamento completo estados-regiões
    """
    try:
        from app.utils.constants import REGIOES_BRASIL, NOMES_ESTADOS
        
        # Organiza mapeamento por região
        mapeamento_por_regiao = {}
        for regiao_id in [1, 2, 3]:
            estados_regiao = region_service.get_estados_por_regiao(regiao_id)
            mapeamento_por_regiao[regiao_id] = {
                'nome': region_service.get_nome_regiao(regiao_id),
                'descricao': region_service.get_descricao_regiao(regiao_id),
                'estados': [
                    {
                        'uf': uf,
                        'nome': NOMES_ESTADOS.get(uf, uf)
                    }
                    for uf in estados_regiao
                ],
                'total_estados': len(estados_regiao)
            }
        
        # Mapeamento direto estado -> região
        mapeamento_estado_regiao = {}
        for uf, regiao_id in REGIOES_BRASIL.items():
            mapeamento_estado_regiao[uf] = {
                'regiao_id': regiao_id,
                'regiao_nome': region_service.get_nome_regiao(regiao_id),
                'estado_nome': NOMES_ESTADOS.get(uf, uf)
            }
        
        resultado = {
            'mapeamento_por_regiao': mapeamento_por_regiao,
            'mapeamento_estado_regiao': mapeamento_estado_regiao,
            'total_estados': len(REGIOES_BRASIL),
            'total_regioes': 3
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message="Mapeamento completo obtido com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@region_bp.route('/validar/<uf>', methods=['GET'])
def validar_estado(uf):
    """
    Valida se uma UF é um estado brasileiro válido
    
    Args:
        uf (str): Sigla do estado
        
    Returns:
        JSON: Resultado da validação
    """
    try:
        uf_upper = uf.upper().strip()
        valido = region_service.validar_estado(uf_upper)
        
        resultado = {
            'uf': uf_upper,
            'valido': valido
        }
        
        if valido:
            regiao_id = region_service.get_regiao_por_estado(uf_upper)
            resultado.update({
                'regiao_id': regiao_id,
                'regiao_nome': region_service.get_nome_regiao(regiao_id)
            })
        
        return jsonify(create_success_response(
            data=resultado,
            message="Validação realizada com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

# Rota de teste
@region_bp.route('/teste', methods=['GET'])
def teste_region():
    """
    Rota de teste para o blueprint de regiões
    
    Returns:
        JSON: Mensagem de teste
    """
    return jsonify(create_success_response(
        data={'blueprint': 'region', 'status': 'funcionando'},
        message="Blueprint de regiões está funcionando corretamente"
    )), HTTP_STATUS['OK']

