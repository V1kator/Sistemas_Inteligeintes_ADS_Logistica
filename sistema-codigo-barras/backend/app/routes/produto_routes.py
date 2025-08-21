"""
Rotas da API para gerenciamento de produtos
"""

from flask import Blueprint, request, jsonify
from app.models import db, Produto
from app.services import CepService, RegionService
from app.utils import ProdutoValidator, create_success_response, create_error_response, paginate_query
from app.utils.constants import HTTP_STATUS, ERROR_MESSAGES, SUCCESS_MESSAGES

# Cria blueprint para rotas de produtos
produto_bp = Blueprint('produto', __name__)

# Instancia serviços
cep_service = CepService()
region_service = RegionService()

@produto_bp.route('/', methods=['POST'])
def criar_produto():
    """
    Cria um novo produto
    
    Body JSON:
        nome (str): Nome do produto
        cep (str): CEP do produto
        estado (str): UF do estado
        cidade (str): Nome da cidade
        descricao (str, opcional): Descrição do produto
        
    Returns:
        JSON: Produto criado ou erro
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify(create_error_response(
                message="Dados JSON são obrigatórios",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Valida dados do produto
        dados_validos, erros = ProdutoValidator.validar_produto(dados)
        if not dados_validos:
            return jsonify(create_error_response(
                message="Dados inválidos",
                status_code=HTTP_STATUS['BAD_REQUEST'],
                errors=erros
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Sanitiza dados
        dados_limpos = ProdutoValidator.sanitizar_dados_produto(dados)
        
        # Consulta CEP para validar se existe
        cep_info = cep_service.consultar_cep_completo(dados_limpos['cep'])
        if not cep_info:
            return jsonify(create_error_response(
                message="CEP não encontrado",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Determina região baseada no estado
        regiao_id = region_service.get_regiao_por_estado(dados_limpos['estado'])
        
        # Cria produto
        produto = Produto(
            nome=dados_limpos['nome'],
            descricao=dados_limpos.get('descricao'),
            cep=dados_limpos['cep_numerico'],
            cep_formatado=dados_limpos['cep'],
            estado=dados_limpos['estado'],
            cidade=dados_limpos['cidade'],
            regiao_id=regiao_id
        )
        
        db.session.add(produto)
        db.session.commit()
        
        return jsonify(create_success_response(
            data=produto.to_dict(),
            message=SUCCESS_MESSAGES['produto_criado'],
            status_code=HTTP_STATUS['CREATED']
        )), HTTP_STATUS['CREATED']
        
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@produto_bp.route('/', methods=['GET'])
def listar_produtos():
    """
    Lista produtos com paginação
    
    Query Parameters:
        page (int): Número da página (padrão: 1)
        per_page (int): Itens por página (padrão: 10, máximo: 100)
        estado (str): Filtrar por estado
        regiao (int): Filtrar por região (1, 2 ou 3)
        
    Returns:
        JSON: Lista paginada de produtos
    """
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Filtros
        estado = request.args.get('estado', '').strip().upper()
        regiao = request.args.get('regiao', type=int)
        
        # Constrói query
        query = Produto.query.filter_by(ativo=True)
        
        if estado:
            query = query.filter(Produto.estado == estado)
        
        if regiao and regiao in [1, 2, 3]:
            query = query.filter(Produto.regiao_id == regiao)
        
        # Ordena por data de criação (mais recentes primeiro)
        query = query.order_by(Produto.data_criacao.desc())
        
        # Aplica paginação
        paginacao = paginate_query(query, page, per_page)
        
        # Formata resultados
        produtos = [produto.to_dict() for produto in paginacao.items]
        
        resultado = {
            'produtos': produtos,
            'paginacao': {
                'page': paginacao.page,
                'per_page': paginacao.per_page,
                'total': paginacao.total,
                'pages': paginacao.pages,
                'has_next': paginacao.has_next,
                'has_prev': paginacao.has_prev
            },
            'filtros': {
                'estado': estado if estado else None,
                'regiao': regiao
            }
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"{len(produtos)} produto(s) encontrado(s)"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@produto_bp.route('/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """
    Obtém um produto específico
    
    Args:
        produto_id (int): ID do produto
        
    Returns:
        JSON: Dados do produto ou erro
    """
    try:
        produto = Produto.query.filter_by(id=produto_id, ativo=True).first()
        
        if not produto:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['produto_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        return jsonify(create_success_response(
            data=produto.to_dict(),
            message="Produto encontrado com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@produto_bp.route('/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """
    Atualiza um produto existente
    
    Args:
        produto_id (int): ID do produto
        
    Body JSON:
        nome (str, opcional): Nome do produto
        cep (str, opcional): CEP do produto
        estado (str, opcional): UF do estado
        cidade (str, opcional): Nome da cidade
        descricao (str, opcional): Descrição do produto
        
    Returns:
        JSON: Produto atualizado ou erro
    """
    try:
        produto = Produto.query.filter_by(id=produto_id, ativo=True).first()
        
        if not produto:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['produto_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        dados = request.get_json()
        
        if not dados:
            return jsonify(create_error_response(
                message="Dados JSON são obrigatórios",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Prepara dados para validação (mantém valores atuais se não fornecidos)
        dados_validacao = {
            'nome': dados.get('nome', produto.nome),
            'cep': dados.get('cep', produto.cep_formatado),
            'estado': dados.get('estado', produto.estado),
            'cidade': dados.get('cidade', produto.cidade),
            'descricao': dados.get('descricao', produto.descricao)
        }
        
        # Valida dados
        dados_validos, erros = ProdutoValidator.validar_produto(dados_validacao)
        if not dados_validos:
            return jsonify(create_error_response(
                message="Dados inválidos",
                status_code=HTTP_STATUS['BAD_REQUEST'],
                errors=erros
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Sanitiza dados
        dados_limpos = ProdutoValidator.sanitizar_dados_produto(dados_validacao)
        
        # Se CEP foi alterado, valida se existe
        if 'cep' in dados and dados['cep'] != produto.cep_formatado:
            cep_info = cep_service.consultar_cep_completo(dados_limpos['cep'])
            if not cep_info:
                return jsonify(create_error_response(
                    message="CEP não encontrado",
                    status_code=HTTP_STATUS['BAD_REQUEST']
                )), HTTP_STATUS['BAD_REQUEST']
        
        # Atualiza campos
        if 'nome' in dados:
            produto.nome = dados_limpos['nome']
        
        if 'descricao' in dados:
            produto.descricao = dados_limpos.get('descricao')
        
        if 'cep' in dados:
            produto.cep = dados_limpos['cep_numerico']
            produto.cep_formatado = dados_limpos['cep']
        
        if 'estado' in dados:
            produto.estado = dados_limpos['estado']
            # Recalcula região se estado mudou
            produto.regiao_id = region_service.get_regiao_por_estado(dados_limpos['estado'])
        
        if 'cidade' in dados:
            produto.cidade = dados_limpos['cidade']
        
        db.session.commit()
        
        return jsonify(create_success_response(
            data=produto.to_dict(),
            message=SUCCESS_MESSAGES['produto_atualizado']
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@produto_bp.route('/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    """
    Deleta um produto (soft delete)
    
    Args:
        produto_id (int): ID do produto
        
    Returns:
        JSON: Resultado da operação
    """
    try:
        produto = Produto.query.filter_by(id=produto_id, ativo=True).first()
        
        if not produto:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['produto_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
        
        # Soft delete
        produto.ativo = False
        db.session.commit()
        
        return jsonify(create_success_response(
            message=SUCCESS_MESSAGES['produto_deletado']
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        db.session.rollback()
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@produto_bp.route('/buscar', methods=['GET'])
def buscar_produtos():
    """
    Busca produtos por nome
    
    Query Parameters:
        q (str): Termo de busca
        page (int): Número da página
        per_page (int): Itens por página
        
    Returns:
        JSON: Lista de produtos encontrados
    """
    try:
        termo = request.args.get('q', '').strip()
        
        if not termo:
            return jsonify(create_error_response(
                message="Termo de busca é obrigatório",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Busca por nome (case insensitive)
        query = Produto.query.filter(
            Produto.ativo == True,
            Produto.nome.ilike(f'%{termo}%')
        ).order_by(Produto.data_criacao.desc())
        
        # Aplica paginação
        paginacao = paginate_query(query, page, per_page)
        
        # Formata resultados
        produtos = [produto.to_dict() for produto in paginacao.items]
        
        resultado = {
            'produtos': produtos,
            'termo_busca': termo,
            'paginacao': {
                'page': paginacao.page,
                'per_page': paginacao.per_page,
                'total': paginacao.total,
                'pages': paginacao.pages,
                'has_next': paginacao.has_next,
                'has_prev': paginacao.has_prev
            }
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message=f"{len(produtos)} produto(s) encontrado(s) para '{termo}'"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

# Rota de teste
@produto_bp.route('/teste', methods=['GET'])
def teste_produto():
    """
    Rota de teste para o blueprint de produtos
    
    Returns:
        JSON: Mensagem de teste
    """
    return jsonify(create_success_response(
        data={'blueprint': 'produto', 'status': 'funcionando'},
        message="Blueprint de produtos está funcionando corretamente"
    )), HTTP_STATUS['OK']

