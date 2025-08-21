"""
Constantes do Sistema de Códigos de Barras por CEP
"""

# Mapeamento de regiões brasileiras por estado
REGIOES_BRASIL = {
    # Norte - Identificador 1
    'AC': 1,  # Acre
    'AP': 1,  # Amapá
    'AM': 1,  # Amazonas
    'PA': 1,  # Pará
    'RO': 1,  # Rondônia
    'RR': 1,  # Roraima
    'TO': 1,  # Tocantins
    
    # Nordeste - Identificador 1
    'AL': 1,  # Alagoas
    'BA': 1,  # Bahia
    'CE': 1,  # Ceará
    'MA': 1,  # Maranhão
    'PB': 1,  # Paraíba
    'PE': 1,  # Pernambuco
    'PI': 1,  # Piauí
    'RN': 1,  # Rio Grande do Norte
    'SE': 1,  # Sergipe
    
    # Centro-Oeste - Identificador 2
    'DF': 2,  # Distrito Federal
    'GO': 2,  # Goiás
    'MT': 2,  # Mato Grosso
    'MS': 2,  # Mato Grosso do Sul
    
    # Sudeste - Identificador 3
    'ES': 3,  # Espírito Santo
    'MG': 3,  # Minas Gerais
    'RJ': 3,  # Rio de Janeiro
    'SP': 3,  # São Paulo
    
    # Sul - Identificador 3
    'PR': 3,  # Paraná
    'RS': 3,  # Rio Grande do Sul
    'SC': 3,  # Santa Catarina
}

# Nomes das regiões por identificador
NOMES_REGIOES = {
    1: 'Norte/Nordeste',
    2: 'Centro-Oeste',
    3: 'Sul/Sudeste'
}

# Descrições das regiões
DESCRICOES_REGIOES = {
    1: 'Região Norte e Nordeste do Brasil',
    2: 'Região Centro-Oeste do Brasil',
    3: 'Região Sul e Sudeste do Brasil'
}

# Estados por região geográfica tradicional
ESTADOS_POR_REGIAO_GEOGRAFICA = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

# Nomes completos dos estados
NOMES_ESTADOS = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

# Formatos de código de barras suportados
FORMATOS_CODIGO_BARRAS = {
    'CODE128': 'Code 128',
    'CODE39': 'Code 39',
    'EAN13': 'EAN-13',
    'EAN8': 'EAN-8',
    'UPCA': 'UPC-A'
}

# Configurações de código de barras
BARCODE_CONFIG = {
    'formato_padrao': 'CODE128',
    'largura_padrao': 2,
    'altura_padrao': 100,
    'tamanho_codigo': 12,  # Caracteres do código base
    'tamanho_codigo_completo': 13,  # Com identificador de região
    'quiet_zone': 6.5,
    'font_size': 10,
    'text_distance': 5.0
}

# Configurações de arquivo
FILE_CONFIG = {
    'extensoes_permitidas': ['.png', '.jpg', '.jpeg'],
    'tamanho_maximo': 16 * 1024 * 1024,  # 16MB
    'formato_imagem_padrao': 'PNG',
    'qualidade_jpeg': 95
}

# Configurações de API
API_CONFIG = {
    'versao': '1.0.0',
    'timeout_padrao': 30,
    'limite_requisicoes_por_minuto': 60,
    'tamanho_pagina_padrao': 10,
    'tamanho_pagina_maximo': 100
}

# URLs de APIs externas
EXTERNAL_APIS = {
    'viacep': {
        'base_url': 'https://viacep.com.br/ws',
        'timeout': 10,
        'formato': 'json'
    }
}

# Mensagens de erro padrão
ERROR_MESSAGES = {
    'cep_invalido': 'CEP inválido. Use o formato 00000-000',
    'cep_nao_encontrado': 'CEP não encontrado',
    'produto_nao_encontrado': 'Produto não encontrado',
    'codigo_barras_nao_encontrado': 'Código de barras não encontrado',
    'arquivo_nao_encontrado': 'Arquivo não encontrado',
    'erro_interno': 'Erro interno do servidor',
    'dados_invalidos': 'Dados fornecidos são inválidos',
    'acesso_negado': 'Acesso negado',
    'metodo_nao_permitido': 'Método não permitido',
    'limite_excedido': 'Limite de requisições excedido'
}

# Mensagens de sucesso padrão
SUCCESS_MESSAGES = {
    'produto_criado': 'Produto criado com sucesso',
    'produto_atualizado': 'Produto atualizado com sucesso',
    'produto_deletado': 'Produto deletado com sucesso',
    'codigo_barras_gerado': 'Código de barras gerado com sucesso',
    'codigo_barras_deletado': 'Código de barras deletado com sucesso',
    'download_registrado': 'Download registrado com sucesso',
    'operacao_realizada': 'Operação realizada com sucesso'
}

# Status HTTP mais utilizados
HTTP_STATUS = {
    'OK': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'METHOD_NOT_ALLOWED': 405,
    'CONFLICT': 409,
    'UNPROCESSABLE_ENTITY': 422,
    'TOO_MANY_REQUESTS': 429,
    'INTERNAL_SERVER_ERROR': 500,
    'SERVICE_UNAVAILABLE': 503
}

# Configurações de log
LOG_CONFIG = {
    'nivel_padrao': 'INFO',
    'formato': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'arquivo_log': 'sistema_codigo_barras.log',
    'tamanho_maximo': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Configurações de cache
CACHE_CONFIG = {
    'ttl_cep': 3600,  # 1 hora em segundos
    'ttl_estatisticas': 300,  # 5 minutos
    'prefixo_chave': 'scb:',  # Sistema Código Barras
    'max_entries': 1000
}

# Padrões de validação
VALIDATION_PATTERNS = {
    'cep': r'^\d{5}-?\d{3}$',
    'uf': r'^[A-Z]{2}$',
    'codigo_barras': r'^[1-3][A-Z0-9]{12}$',
    'nome_produto': r'^[a-zA-ZÀ-ÿ0-9\s\-_\.]{2,200}$',
    'nome_arquivo': r'^[a-zA-Z0-9\-_\.]{1,100}$'
}

# Configurações de desenvolvimento
DEV_CONFIG = {
    'debug': True,
    'reload': True,
    'host': '0.0.0.0',
    'port': 5000,
    'workers': 1
}

# Configurações de produção
PROD_CONFIG = {
    'debug': False,
    'reload': False,
    'host': '0.0.0.0',
    'port': 5000,
    'workers': 4
}

