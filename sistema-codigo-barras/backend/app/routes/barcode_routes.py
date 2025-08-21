"""
Rotas da API para geração e gerenciamento de códigos de barras
"""

import os
from flask import Blueprint, request, jsonify, send_file
from app.models import db, Produto, CodigoBarras
from app.services import BarcodeService
from app.utils import CodigoBarsValidator, create_success_response, create_error_response, paginate_query
from app.utils.constants import HTTP_STATUS, ERROR_MESSAGES, SUCCESS_MESSAGES

# Cria blueprint para rotas de códigos de barras
barcode_bp = Blueprint('barcode', __name__)

# Instancia serviços
barcode_service = BarcodeService()

@barcode_bp.route('/gerar', methods=['POST'])
def gerar_codigo_barras():
    """
    Gera um novo código de barras para um produto
    
    Body JSON:
        produto_id (int): ID do produto
        regiao_id (int, opcional): ID da região (se não fornecido, usa a região do produto)
        
    Returns:
        JSON: Código de barras gerado ou erro
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify(create_error_response(
                message="Dados JSON são obrigatórios",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        produto_id = dados.get('produto_id')
        regiao_id = dados.get('regiao_id')
        
        if not produto_id:
            return jsonify(create_error_response(
                message="ID do produto é obrigatório",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Verifica se produto existe
        produto = Produto.query.filter_by(id=produto_id, ativo=True).first()
        if not produto:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['produto_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        # Valida região se fornecida
        if regiao_id and regiao_id not in [1, 2, 3]:
            return jsonify(create_error_response(
                message="Região deve ser 1, 2 ou 3",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Gera código de barras completo
        codigo_barras = barcode_service.criar_codigo_barras_completo(produto_id, regiao_id)
        
        if not codigo_barras:
            return jsonify(create_error_response(
                message="Erro ao gerar código de barras",
                status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR']
            )), HTTP_STATUS['INTERNAL_SERVER_ERROR']
        
        return jsonify(create_success_response(
            data=codigo_barras.to_dict(),
            message=SUCCESS_MESSAGES['codigo_barras_gerado'],
            status_code=HTTP_STATUS['CREATED']
        )), HTTP_STATUS['CREATED']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/<int:codigo_id>', methods=['GET'])
def obter_codigo_barras(codigo_id):
    """
    Obtém informações de um código de barras
    
    Args:
        codigo_id (int): ID do código de barras
        
    Returns:
        JSON: Dados do código de barras ou erro
    """
    try:
        codigo_barras = barcode_service.buscar_codigo_barras(codigo_id)
        
        if not codigo_barras:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['codigo_barras_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        return jsonify(create_success_response(
            data=codigo_barras.to_dict(),
            message="Código de barras encontrado com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/buscar/<codigo_completo>', methods=['GET'])
def buscar_por_codigo(codigo_completo):
    """
    Busca código de barras pelo código completo
    
    Args:
        codigo_completo (str): Código completo do código de barras
        
    Returns:
        JSON: Dados do código de barras ou erro
    """
    try:
        # Valida formato do código
        codigo_valido, erro_validacao = CodigoBarsValidator.validar_codigo_completo(codigo_completo)
        if not codigo_valido:
            return jsonify(create_error_response(
                message=f"Código inválido: {erro_validacao}",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        codigo_barras = barcode_service.buscar_por_codigo_completo(codigo_completo)
        
        if not codigo_barras:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['codigo_barras_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        return jsonify(create_success_response(
            data=codigo_barras.to_dict(),
            message="Código de barras encontrado com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/produto/<int:produto_id>', methods=['GET'])
def listar_codigos_produto(produto_id):
    """
    Lista todos os códigos de barras de um produto
    
    Args:
        produto_id (int): ID do produto
        
    Returns:
        JSON: Lista de códigos de barras do produto
    """
    try:
        # Verifica se produto existe
        produto = Produto.query.filter_by(id=produto_id, ativo=True).first()
        if not produto:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['produto_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        codigos = barcode_service.listar_codigos_produto(produto_id)
        
        resultado = {
            'produto': produto.to_dict(),
            'codigos_barras': codigos,
            'total_codigos': len(codigos)
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"{len(codigos)} código(s) de barras encontrado(s) para o produto"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/download/<int:codigo_id>', methods=['GET'])
def download_codigo_barras(codigo_id):
    """
    Faz download do arquivo PNG do código de barras
    
    Args:
        codigo_id (int): ID do código de barras
        
    Returns:
        File: Arquivo PNG do código de barras
    """
    try:
        # Busca código de barras
        codigo_barras = barcode_service.buscar_codigo_barras(codigo_id)
        
        if not codigo_barras:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['codigo_barras_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        # Obtém caminho do arquivo
        caminho_arquivo = barcode_service.get_caminho_arquivo(codigo_id)
        
        if not caminho_arquivo:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['arquivo_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        # Registra download
        barcode_service.registrar_download(codigo_id)
        
        # Envia arquivo
        return send_file(
            caminho_arquivo,
            as_attachment=True,
            download_name=f"codigo_barras_{codigo_barras.codigo_completo}.png",
            mimetype='image/png'
        )
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/', methods=['GET'])
def listar_codigos_barras():
    """
    Lista códigos de barras com paginação
    
    Query Parameters:
        page (int): Número da página (padrão: 1)
        per_page (int): Itens por página (padrão: 10, máximo: 100)
        regiao (int): Filtrar por região (1, 2 ou 3)
        
    Returns:
        JSON: Lista paginada de códigos de barras
    """
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Filtros
        regiao = request.args.get('regiao', type=int)
        
        # Constrói query
        query = CodigoBarras.query.filter_by(ativo=True)
        
        if regiao and regiao in [1, 2, 3]:
            query = query.filter(CodigoBarras.regiao_identificador == regiao)
        
        # Ordena por data de criação (mais recentes primeiro)
        query = query.order_by(CodigoBarras.data_criacao.desc())
        
        # Aplica paginação
        paginacao = paginate_query(query, page, per_page)
        
        # Formata resultados
        codigos = [codigo.to_dict() for codigo in paginacao.items]
        
        resultado = {
            'codigos_barras': codigos,
            'paginacao': {
                'page': paginacao.page,
                'per_page': paginacao.per_page,
                'total': paginacao.total,
                'pages': paginacao.pages,
                'has_next': paginacao.has_next,
                'has_prev': paginacao.has_prev
            },
            'filtros': {
                'regiao': regiao
            }
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"{len(codigos)} código(s) de barras encontrado(s)"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/<int:codigo_id>', methods=['DELETE'])
def deletar_codigo_barras(codigo_id):
    """
    Deleta um código de barras (soft delete)
    
    Args:
        codigo_id (int): ID do código de barras
        
    Returns:
        JSON: Resultado da operação
    """
    try:
        sucesso = barcode_service.deletar_codigo_barras(codigo_id)
        
        if not sucesso:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['codigo_barras_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        return jsonify(create_success_response(
            message=SUCCESS_MESSAGES['codigo_barras_deletado']
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@barcode_bp.route('/validar/<codigo_completo>', methods=['GET'])
def validar_codigo(codigo_completo):
    """
    Valida formato de um código de barras
    
    Args:
        codigo_completo (str): Código completo a ser validado
        
    Returns:
        JSON: Resultado da validação
    """
    try:
        codigo_valido, erro_validacao = CodigoBarsValidator.validar_codigo_completo(codigo_completo)
        regiao_id = CodigoBarsValidator.extrair_regiao_codigo(codigo_completo)
        
        resultado = {
            'codigo': codigo_completo,
            'valido': codigo_valido,
            'erro': erro_validacao if not codigo_valido else None,
            'regiao_id': regiao_id,
            'codigo_base': codigo_completo[1:] if len(codigo_completo) > 1 else None
        }
        
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

@barcode_bp.route('/stats', methods=['GET'])
def estatisticas_codigos():
    """
    Retorna estatísticas dos códigos de barras
    
    Returns:
        JSON: Estatísticas dos códigos de barras
    """
    try:
        stats = barcode_service.get_estatisticas()
        
        return jsonify(create_success_response(
            data=stats,
            message="Estatísticas obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

# Rota de teste
@barcode_bp.route('/teste', methods=['GET'])
def teste_barcode():
    """
    Rota de teste para o blueprint de códigos de barras
    
    Returns:
        JSON: Mensagem de teste
    """
    return jsonify(create_success_response(
        data={'blueprint': 'barcode', 'status': 'funcionando'},
        message="Blueprint de códigos de barras está funcionando corretamente"
    )), HTTP_STATUS['OK']

