"""
Serviço para consulta de CEP usando a API ViaCEP
"""

import requests
import re
from typing import Dict, Optional, Tuple
from app.models import db, CepRegiao
from config import Config

class CepService:
    """Serviço para consulta e validação de CEPs brasileiros"""
    
    def __init__(self):
        self.api_url = Config.CEP_API_URL
        self.timeout = Config.CEP_API_TIMEOUT
    
    def validar_cep(self, cep: str) -> Tuple[bool, str]:
        """
        Valida formato do CEP brasileiro
        
        Args:
            cep (str): CEP a ser validado
            
        Returns:
            Tuple[bool, str]: (é_válido, cep_limpo)
        """
        if not cep:
            return False, ""
        
        # Remove caracteres não numéricos
        cep_limpo = re.sub(r'[^0-9]', '', cep.strip())
        
        # Verifica se tem exatamente 8 dígitos
        if len(cep_limpo) != 8:
            return False, cep_limpo
        
        # Verifica se não é um CEP inválido conhecido
        ceps_invalidos = ['00000000', '11111111', '22222222', '33333333', 
                         '44444444', '55555555', '66666666', '77777777', 
                         '88888888', '99999999']
        
        if cep_limpo in ceps_invalidos:
            return False, cep_limpo
        
        return True, cep_limpo
    
    def formatar_cep(self, cep: str) -> str:
        """
        Formata CEP no padrão 00000-000
        
        Args:
            cep (str): CEP apenas números
            
        Returns:
            str: CEP formatado
        """
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep
    
    def consultar_cep_cache(self, cep: str) -> Optional[Dict]:
        """
        Consulta CEP no cache local (banco de dados)
        
        Args:
            cep (str): CEP a ser consultado
            
        Returns:
            Optional[Dict]: Dados do CEP se encontrado no cache
        """
        valido, cep_limpo = self.validar_cep(cep)
        if not valido:
            return None
        
        cep_regiao = CepRegiao.buscar_por_cep(cep_limpo)
        if cep_regiao:
            return cep_regiao.to_dict()
        
        return None
    
    def consultar_cep_api(self, cep: str) -> Optional[Dict]:
        """
        Consulta CEP na API ViaCEP
        
        Args:
            cep (str): CEP a ser consultado
            
        Returns:
            Optional[Dict]: Dados do CEP da API
        """
        valido, cep_limpo = self.validar_cep(cep)
        if not valido:
            return None
        
        try:
            # Formata CEP para a API
            cep_formatado = self.formatar_cep(cep_limpo)
            url = f"{self.api_url}/{cep_formatado}/json/"
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            dados = response.json()
            
            # Verifica se a API retornou erro
            if dados.get('erro'):
                return None
            
            # Padroniza os dados
            dados_padronizados = {
                'cep': dados.get('cep', cep_formatado),
                'logradouro': dados.get('logradouro', ''),
                'complemento': dados.get('complemento', ''),
                'bairro': dados.get('bairro', ''),
                'localidade': dados.get('localidade', ''),
                'uf': dados.get('uf', ''),
                'ibge': dados.get('ibge', ''),
                'gia': dados.get('gia', ''),
                'ddd': dados.get('ddd', ''),
                'siafi': dados.get('siafi', '')
            }
            
            return dados_padronizados
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar CEP na API: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao consultar CEP: {e}")
            return None
    
    def salvar_cep_cache(self, dados_cep: Dict) -> Optional[CepRegiao]:
        """
        Salva dados de CEP no cache local
        
        Args:
            dados_cep (Dict): Dados do CEP da API
            
        Returns:
            Optional[CepRegiao]: Registro salvo no cache
        """
        try:
            cep_regiao = CepRegiao.criar_de_dados_cep(dados_cep)
            db.session.add(cep_regiao)
            db.session.commit()
            return cep_regiao
        except Exception as e:
            print(f"Erro ao salvar CEP no cache: {e}")
            db.session.rollback()
            return None
    
    def consultar_cep_completo(self, cep: str) -> Optional[Dict]:
        """
        Consulta CEP completa: primeiro no cache, depois na API
        
        Args:
            cep (str): CEP a ser consultado
            
        Returns:
            Optional[Dict]: Dados completos do CEP com região
        """
        # Primeiro tenta no cache
        dados_cache = self.consultar_cep_cache(cep)
        if dados_cache:
            return dados_cache
        
        # Se não encontrou no cache, consulta na API
        dados_api = self.consultar_cep_api(cep)
        if not dados_api:
            return None
        
        # Salva no cache para consultas futuras
        cep_regiao = self.salvar_cep_cache(dados_api)
        if cep_regiao:
            return cep_regiao.to_dict()
        
        # Se não conseguiu salvar no cache, retorna dados da API com região
        from .region_service import RegionService
        region_service = RegionService()
        
        estado = dados_api.get('uf', '')
        regiao_id = region_service.get_regiao_por_estado(estado)
        regiao_nome = region_service.get_nome_regiao(regiao_id)
        
        dados_completos = {
            'cep': dados_api.get('cep'),
            'cep_numerico': re.sub(r'[^0-9]', '', dados_api.get('cep', '')),
            'estado': estado,
            'cidade': dados_api.get('localidade', ''),
            'bairro': dados_api.get('bairro', ''),
            'logradouro': dados_api.get('logradouro', ''),
            'regiao_id': regiao_id,
            'regiao_nome': regiao_nome,
            'fonte_dados': 'ViaCEP'
        }
        
        return dados_completos
    
    def buscar_ceps_por_endereco(self, estado: str, cidade: str, logradouro: str) -> Optional[list]:
        """
        Busca CEPs por endereço (busca reversa)
        
        Args:
            estado (str): UF do estado
            cidade (str): Nome da cidade
            logradouro (str): Nome do logradouro
            
        Returns:
            Optional[list]: Lista de CEPs encontrados
        """
        try:
            url = f"{self.api_url}/{estado}/{cidade}/{logradouro}/json/"
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            dados = response.json()
            
            if isinstance(dados, list) and len(dados) > 0:
                return dados
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar CEPs por endereço: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar CEPs por endereço: {e}")
            return None
    
    def get_estatisticas_cache(self) -> Dict:
        """
        Retorna estatísticas do cache de CEPs
        
        Returns:
            Dict: Estatísticas do cache
        """
        try:
            total_ceps = CepRegiao.query.filter_by(ativo=True).count()
            stats_regioes = CepRegiao.get_estatisticas_regioes()
            
            return {
                'total_ceps_cache': total_ceps,
                'estatisticas_regioes': stats_regioes,
                'fonte_dados': 'ViaCEP'
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas do cache: {e}")
            return {
                'total_ceps_cache': 0,
                'estatisticas_regioes': [],
                'erro': str(e)
            }

