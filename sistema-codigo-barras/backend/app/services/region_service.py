"""
Serviço para identificação e gerenciamento de regiões brasileiras
"""

from typing import Dict, List, Optional
from config import Config

class RegionService:
    """Serviço para gerenciar regiões brasileiras e seus identificadores"""
    
    def __init__(self):
        self.regioes_brasil = Config.REGIOES_BRASIL
    
    def get_regiao_por_estado(self, uf: str) -> int:
        """
        Retorna o identificador da região baseado na UF do estado
        
        Args:
            uf (str): Sigla do estado (UF)
            
        Returns:
            int: Identificador da região (1, 2 ou 3)
        """
        if not uf:
            return 1  # Default para Norte/Nordeste
        
        uf_upper = uf.upper().strip()
        return self.regioes_brasil.get(uf_upper, 1)
    
    def get_nome_regiao(self, regiao_id: int) -> str:
        """
        Retorna o nome da região baseado no identificador
        
        Args:
            regiao_id (int): Identificador da região
            
        Returns:
            str: Nome da região
        """
        nomes_regioes = {
            1: 'Norte/Nordeste',
            2: 'Centro-Oeste',
            3: 'Sul/Sudeste'
        }
        return nomes_regioes.get(regiao_id, 'Desconhecida')
    
    def get_descricao_regiao(self, regiao_id: int) -> str:
        """
        Retorna descrição detalhada da região
        
        Args:
            regiao_id (int): Identificador da região
            
        Returns:
            str: Descrição da região
        """
        descricoes = {
            1: 'Região Norte e Nordeste do Brasil',
            2: 'Região Centro-Oeste do Brasil',
            3: 'Região Sul e Sudeste do Brasil'
        }
        return descricoes.get(regiao_id, 'Região não identificada')
    
    def get_estados_por_regiao(self, regiao_id: int) -> List[str]:
        """
        Retorna lista de estados de uma região
        
        Args:
            regiao_id (int): Identificador da região
            
        Returns:
            List[str]: Lista de UFs da região
        """
        estados_regiao = []
        for uf, id_regiao in self.regioes_brasil.items():
            if id_regiao == regiao_id:
                estados_regiao.append(uf)
        
        return sorted(estados_regiao)
    
    def get_todas_regioes(self) -> List[Dict]:
        """
        Retorna informações de todas as regiões
        
        Returns:
            List[Dict]: Lista com dados de todas as regiões
        """
        regioes = []
        for regiao_id in [1, 2, 3]:
            regioes.append({
                'id': regiao_id,
                'nome': self.get_nome_regiao(regiao_id),
                'descricao': self.get_descricao_regiao(regiao_id),
                'estados': self.get_estados_por_regiao(regiao_id),
                'total_estados': len(self.get_estados_por_regiao(regiao_id))
            })
        
        return regioes
    
    def validar_estado(self, uf: str) -> bool:
        """
        Valida se a UF é um estado brasileiro válido
        
        Args:
            uf (str): Sigla do estado
            
        Returns:
            bool: True se é válido
        """
        if not uf:
            return False
        
        return uf.upper().strip() in self.regioes_brasil
    
    def get_regiao_detalhada(self, regiao_id: int) -> Optional[Dict]:
        """
        Retorna informações detalhadas de uma região específica
        
        Args:
            regiao_id (int): Identificador da região
            
        Returns:
            Optional[Dict]: Dados detalhados da região
        """
        if regiao_id not in [1, 2, 3]:
            return None
        
        estados = self.get_estados_por_regiao(regiao_id)
        
        # Mapeia estados para nomes completos (alguns exemplos)
        nomes_estados = {
            # Norte
            'AC': 'Acre', 'AP': 'Amapá', 'AM': 'Amazonas', 'PA': 'Pará',
            'RO': 'Rondônia', 'RR': 'Roraima', 'TO': 'Tocantins',
            # Nordeste
            'AL': 'Alagoas', 'BA': 'Bahia', 'CE': 'Ceará', 'MA': 'Maranhão',
            'PB': 'Paraíba', 'PE': 'Pernambuco', 'PI': 'Piauí', 'RN': 'Rio Grande do Norte', 'SE': 'Sergipe',
            # Centro-Oeste
            'DF': 'Distrito Federal', 'GO': 'Goiás', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
            # Sudeste
            'ES': 'Espírito Santo', 'MG': 'Minas Gerais', 'RJ': 'Rio de Janeiro', 'SP': 'São Paulo',
            # Sul
            'PR': 'Paraná', 'RS': 'Rio Grande do Sul', 'SC': 'Santa Catarina'
        }
        
        estados_detalhados = []
        for uf in estados:
            estados_detalhados.append({
                'uf': uf,
                'nome': nomes_estados.get(uf, uf)
            })
        
        return {
            'id': regiao_id,
            'nome': self.get_nome_regiao(regiao_id),
            'descricao': self.get_descricao_regiao(regiao_id),
            'estados': estados_detalhados,
            'total_estados': len(estados),
            'identificador_codigo_barras': regiao_id
        }
    
    def get_estatisticas_regioes(self) -> Dict:
        """
        Retorna estatísticas gerais das regiões
        
        Returns:
            Dict: Estatísticas das regiões
        """
        total_estados = len(self.regioes_brasil)
        regioes_stats = {}
        
        for regiao_id in [1, 2, 3]:
            estados_regiao = self.get_estados_por_regiao(regiao_id)
            regioes_stats[regiao_id] = {
                'nome': self.get_nome_regiao(regiao_id),
                'total_estados': len(estados_regiao),
                'percentual': round((len(estados_regiao) / total_estados) * 100, 2)
            }
        
        return {
            'total_estados_brasil': total_estados,
            'total_regioes': 3,
            'regioes': regioes_stats,
            'mapeamento_identificadores': {
                '1': 'Norte/Nordeste',
                '2': 'Centro-Oeste',
                '3': 'Sul/Sudeste'
            }
        }
    
    def buscar_regiao_por_nome(self, nome: str) -> Optional[Dict]:
        """
        Busca região por nome ou parte do nome
        
        Args:
            nome (str): Nome ou parte do nome da região
            
        Returns:
            Optional[Dict]: Dados da região encontrada
        """
        if not nome:
            return None
        
        nome_lower = nome.lower().strip()
        
        # Busca por correspondência no nome
        for regiao_id in [1, 2, 3]:
            nome_regiao = self.get_nome_regiao(regiao_id).lower()
            if nome_lower in nome_regiao or nome_regiao in nome_lower:
                return self.get_regiao_detalhada(regiao_id)
        
        # Busca por correspondência em palavras-chave
        palavras_chave = {
            1: ['norte', 'nordeste', 'amazonia', 'sertao'],
            2: ['centro', 'oeste', 'pantanal', 'cerrado'],
            3: ['sul', 'sudeste', 'serra', 'mata atlantica']
        }
        
        for regiao_id, palavras in palavras_chave.items():
            for palavra in palavras:
                if palavra in nome_lower:
                    return self.get_regiao_detalhada(regiao_id)
        
        return None

