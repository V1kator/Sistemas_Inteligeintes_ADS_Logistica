"""
Validadores de dados para o Sistema de Códigos de Barras por CEP
"""

import re
from typing import Dict, List, Tuple, Any

class CepValidator:
    """Validador para CEPs brasileiros"""
    
    @staticmethod
    def validar_formato(cep: str) -> Tuple[bool, str]:
        """
        Valida formato do CEP
        
        Args:
            cep (str): CEP a ser validado
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem_erro)
        """
        if not cep:
            return False, "CEP é obrigatório"
        
        # Remove espaços e caracteres especiais
        cep_limpo = re.sub(r'[^0-9]', '', cep.strip())
        
        if len(cep_limpo) != 8:
            return False, "CEP deve ter exatamente 8 dígitos"
        
        # Verifica se não é um CEP inválido conhecido
        ceps_invalidos = [
            '00000000', '11111111', '22222222', '33333333',
            '44444444', '55555555', '66666666', '77777777',
            '88888888', '99999999'
        ]
        
        if cep_limpo in ceps_invalidos:
            return False, "CEP inválido"
        
        return True, ""
    
    @staticmethod
    def formatar_cep(cep: str) -> str:
        """
        Formata CEP no padrão 00000-000
        
        Args:
            cep (str): CEP apenas números
            
        Returns:
            str: CEP formatado
        """
        cep_limpo = re.sub(r'[^0-9]', '', cep.strip())
        if len(cep_limpo) == 8:
            return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
        return cep
    
    @staticmethod
    def limpar_cep(cep: str) -> str:
        """
        Remove formatação do CEP
        
        Args:
            cep (str): CEP formatado
            
        Returns:
            str: CEP apenas números
        """
        return re.sub(r'[^0-9]', '', cep.strip())

class ProdutoValidator:
    """Validador para dados de produtos"""
    
    @staticmethod
    def validar_produto(dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados completos de um produto
        
        Args:
            dados (Dict): Dados do produto
            
        Returns:
            Tuple[bool, List[str]]: (é_válido, lista_erros)
        """
        erros = []
        
        # Valida nome
        nome = dados.get('nome', '').strip()
        if not nome:
            erros.append("Nome do produto é obrigatório")
        elif len(nome) < 2:
            erros.append("Nome do produto deve ter pelo menos 2 caracteres")
        elif len(nome) > 200:
            erros.append("Nome do produto deve ter no máximo 200 caracteres")
        
        # Valida CEP
        cep = dados.get('cep', '')
        cep_valido, erro_cep = CepValidator.validar_formato(cep)
        if not cep_valido:
            erros.append(f"CEP inválido: {erro_cep}")
        
        # Valida estado
        estado = dados.get('estado', '').strip().upper()
        if not estado:
            erros.append("Estado (UF) é obrigatório")
        elif len(estado) != 2:
            erros.append("Estado deve ter exatamente 2 caracteres")
        elif not ProdutoValidator.validar_uf(estado):
            erros.append("Estado (UF) inválido")
        
        # Valida cidade
        cidade = dados.get('cidade', '').strip()
        if not cidade:
            erros.append("Cidade é obrigatória")
        elif len(cidade) < 2:
            erros.append("Nome da cidade deve ter pelo menos 2 caracteres")
        elif len(cidade) > 100:
            erros.append("Nome da cidade deve ter no máximo 100 caracteres")
        
        # Valida descrição (opcional)
        descricao = dados.get('descricao', '')
        if descricao and len(descricao) > 1000:
            erros.append("Descrição deve ter no máximo 1000 caracteres")
        
        return len(erros) == 0, erros
    
    @staticmethod
    def validar_uf(uf: str) -> bool:
        """
        Valida se a UF é um estado brasileiro válido
        
        Args:
            uf (str): Sigla do estado
            
        Returns:
            bool: True se é válido
        """
        ufs_validas = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }
        return uf.upper().strip() in ufs_validas
    
    @staticmethod
    def sanitizar_dados_produto(dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitiza e limpa dados do produto
        
        Args:
            dados (Dict): Dados brutos do produto
            
        Returns:
            Dict: Dados sanitizados
        """
        dados_limpos = {}
        
        # Nome
        if 'nome' in dados:
            dados_limpos['nome'] = dados['nome'].strip()
        
        # Descrição
        if 'descricao' in dados:
            dados_limpos['descricao'] = dados['descricao'].strip() if dados['descricao'] else None
        
        # CEP
        if 'cep' in dados:
            cep_limpo = CepValidator.limpar_cep(dados['cep'])
            dados_limpos['cep'] = CepValidator.formatar_cep(cep_limpo)
            dados_limpos['cep_numerico'] = cep_limpo
        
        # Estado
        if 'estado' in dados:
            dados_limpos['estado'] = dados['estado'].strip().upper()
        
        # Cidade
        if 'cidade' in dados:
            dados_limpos['cidade'] = dados['cidade'].strip().title()
        
        return dados_limpos

class CodigoBarsValidator:
    """Validador para códigos de barras"""
    
    @staticmethod
    def validar_codigo_completo(codigo: str) -> Tuple[bool, str]:
        """
        Valida formato do código completo
        
        Args:
            codigo (str): Código completo a ser validado
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem_erro)
        """
        if not codigo:
            return False, "Código é obrigatório"
        
        codigo_limpo = codigo.strip().upper()
        
        # Deve ter 13 caracteres (1 dígito região + 12 código)
        if len(codigo_limpo) != 13:
            return False, "Código deve ter exatamente 13 caracteres"
        
        # Primeiro caractere deve ser 1, 2 ou 3 (região)
        if codigo_limpo[0] not in ['1', '2', '3']:
            return False, "Primeiro dígito deve ser 1, 2 ou 3 (identificador de região)"
        
        # Restante deve ser alfanumérico
        codigo_base = codigo_limpo[1:]
        if not re.match(r'^[A-Z0-9]{12}$', codigo_base):
            return False, "Código deve conter apenas letras maiúsculas e números"
        
        return True, ""
    
    @staticmethod
    def extrair_regiao_codigo(codigo: str) -> int:
        """
        Extrai identificador de região do código
        
        Args:
            codigo (str): Código completo
            
        Returns:
            int: Identificador da região (1, 2 ou 3)
        """
        if not codigo or len(codigo) < 1:
            return 1  # Default
        
        try:
            regiao = int(codigo[0])
            return regiao if regiao in [1, 2, 3] else 1
        except (ValueError, IndexError):
            return 1

class ApiValidator:
    """Validador para dados de API"""
    
    @staticmethod
    def validar_parametros_busca(params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida parâmetros de busca da API
        
        Args:
            params (Dict): Parâmetros da requisição
            
        Returns:
            Tuple[bool, List[str]]: (é_válido, lista_erros)
        """
        erros = []
        
        # Valida página
        if 'page' in params:
            try:
                page = int(params['page'])
                if page < 1:
                    erros.append("Página deve ser maior que 0")
            except (ValueError, TypeError):
                erros.append("Página deve ser um número inteiro")
        
        # Valida limite
        if 'limit' in params:
            try:
                limit = int(params['limit'])
                if limit < 1:
                    erros.append("Limite deve ser maior que 0")
                elif limit > 100:
                    erros.append("Limite deve ser no máximo 100")
            except (ValueError, TypeError):
                erros.append("Limite deve ser um número inteiro")
        
        # Valida ordenação
        if 'sort' in params:
            sorts_validos = ['id', 'nome', 'data_criacao', 'data_atualizacao']
            if params['sort'] not in sorts_validos:
                erros.append(f"Ordenação deve ser um dos valores: {', '.join(sorts_validos)}")
        
        # Valida direção da ordenação
        if 'order' in params:
            if params['order'].lower() not in ['asc', 'desc']:
                erros.append("Direção da ordenação deve ser 'asc' ou 'desc'")
        
        return len(erros) == 0, erros

