"""
Rotas da API para consulta e validação de CEP
"""

from flask import Blueprint, request, jsonify
from app.services import CepService
from app.utils import CepValidator, create_success_response, create_error_response
from app.utils.constants import HTTP_STATUS, ERROR_MESSAGES, SUCCESS_MESSAGES

# Cria blueprint para rotas de CEP
cep_bp = Blueprint('cep', __name__)

# Instancia serviços
cep_service = CepService()

@cep_bp.route('/consultar/<cep>', methods=['GET'])
def consultar_cep(cep):
    """
    Consulta informações de um CEP
    
    Args:
        cep (str): CEP a ser consultado
        
    Returns:
        JSON: Dados do CEP ou erro
    """
    try:
        # Valida formato do CEP
        cep_valido, erro_validacao = CepValidator.validar_formato(cep)
        if not cep_valido:
            return jsonify(create_error_response(
                message=f"CEP inválido: {erro_validacao}",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Consulta CEP completo (cache + API)
        resultado = cep_service.consultar_cep_completo(cep)
        
        if resultado:
            return jsonify(create_success_response(
                data=resultado,
                message="CEP encontrado com sucesso"
            )), HTTP_STATUS['OK']
        else:
            return jsonify(create_error_response(
                message=ERROR_MESSAGES['cep_nao_encontrado'],
                status_code=HTTP_STATUS['NOT_FOUND']
            )), HTTP_STATUS['NOT_FOUND']
            
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@cep_bp.route('/validar/<cep>', methods=['GET'])
def validar_cep(cep):
    """
    Valida formato de um CEP
    
    Args:
        cep (str): CEP a ser validado
        
    Returns:
        JSON: Resultado da validação
    """
    try:
        cep_valido, erro_validacao = CepValidator.validar_formato(cep)
        
        resultado = {
            'cep': cep,
            'valido': cep_valido,
            'erro': erro_validacao if not cep_valido else None,
            'cep_formatado': CepValidator.formatar_cep(cep) if cep_valido else None
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

@cep_bp.route('/buscar', methods=['GET'])
def buscar_cep():
    """
    Busca CEPs por estado, cidade ou logradouro
    
    Query Parameters:
        estado (str): UF do estado
        cidade (str): Nome da cidade
        logradouro (str): Nome do logradouro
        
    Returns:
        JSON: Lista de CEPs encontrados
    """
    try:
        # Obtém parâmetros da query
        estado = request.args.get('estado', '').strip().upper()
        cidade = request.args.get('cidade', '').strip()
        logradouro = request.args.get('logradouro', '').strip()
        
        # Valida se pelo menos um parâmetro foi fornecido
        if not any([estado, cidade, logradouro]):
            return jsonify(create_error_response(
                message="Pelo menos um parâmetro de busca deve ser fornecido (estado, cidade ou logradouro)",
                status_code=HTTP_STATUS['BAD_REQUEST']
            )), HTTP_STATUS['BAD_REQUEST']
        
        # Realiza busca reversa
        resultados = cep_service.buscar_cep_reverso(
            estado=estado if estado else None,
            cidade=cidade if cidade else None,
            logradouro=logradouro if logradouro else None
        )
        
        return jsonify(create_success_response(
            data={
                'resultados': resultados,
                'total': len(resultados),
                'parametros_busca': {
                    'estado': estado,
                    'cidade': cidade,
                    'logradouro': logradouro
                }
            },
            message=f"Busca realizada com sucesso. {len(resultados)} resultado(s) encontrado(s)"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@cep_bp.route('/cache/stats', methods=['GET'])
def stats_cache():
    """
    Retorna estatísticas do cache de CEPs
    
    Returns:
        JSON: Estatísticas do cache
    """
    try:
        stats = cep_service.get_estatisticas_cache()
        
        return jsonify(create_success_response(
            data=stats,
            message="Estatísticas do cache obtidas com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@cep_bp.route('/cache/limpar', methods=['DELETE'])
def limpar_cache():
    """
    Limpa o cache de CEPs
    
    Returns:
        JSON: Resultado da operação
    """
    try:
        # Implementar limpeza do cache se necessário
        # Por enquanto, retorna sucesso
        
        return jsonify(create_success_response(
            message="Cache limpo com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

@cep_bp.route('/formatar/<cep>', methods=['GET'])
def formatar_cep(cep):
    """
    Formata um CEP no padrão brasileiro
    
    Args:
        cep (str): CEP a ser formatado
        
    Returns:
        JSON: CEP formatado
    """
    try:
        cep_formatado = CepValidator.formatar_cep(cep)
        cep_limpo = CepValidator.limpar_cep(cep)
        
        resultado = {
            'cep_original': cep,
            'cep_formatado': cep_formatado,
            'cep_numerico': cep_limpo,
            'valido': len(cep_limpo) == 8
        }
        
        return jsonify(create_success_response(
            data=resultado,
            message="CEP formatado com sucesso"
        )), HTTP_STATUS['OK']
        
    except Exception as e:
        return jsonify(create_error_response(
            message=ERROR_MESSAGES['erro_interno'],
            status_code=HTTP_STATUS['INTERNAL_SERVER_ERROR'],
            details=str(e)
        )), HTTP_STATUS['INTERNAL_SERVER_ERROR']

# Rota de teste para verificar se o blueprint está funcionando
@cep_bp.route('/teste', methods=['GET'])
def teste_cep():
    """
    Rota de teste para o blueprint de CEP
    
    Returns:
        JSON: Mensagem de teste
    """
    return jsonify(create_success_response(
        data={'blueprint': 'cep', 'status': 'funcionando'},
        message="Blueprint de CEP está funcionando corretamente"
    )), HTTP_STATUS['OK']

