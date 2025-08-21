"""
Serviço para geração e gerenciamento de códigos de barras
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Optional, Tuple
from io import BytesIO

import barcode
from barcode.writer import ImageWriter
from PIL import Image

from app.models import db, CodigoBarras, Produto
from config import Config

class BarcodeService:
    """Serviço para geração e gerenciamento de códigos de barras"""
    
    def __init__(self):
        self.formato = Config.BARCODE_FORMAT
        self.largura = Config.BARCODE_WIDTH
        self.altura = Config.BARCODE_HEIGHT
        self.pasta_uploads = Config.UPLOAD_FOLDER
        
        # Garante que a pasta de uploads existe
        os.makedirs(self.pasta_uploads, exist_ok=True)
    
    def gerar_codigo_unico(self) -> str:
        """
        Gera um código único para o código de barras
        
        Returns:
            str: Código único de 12 caracteres
        """
        # Gera UUID e pega os primeiros 12 caracteres alfanuméricos
        codigo_base = str(uuid.uuid4()).replace('-', '')[:12].upper()
        
        # Verifica se já existe no banco (muito improvável, mas por segurança)
        while CodigoBarras.query.filter_by(codigo=codigo_base).first():
            codigo_base = str(uuid.uuid4()).replace('-', '')[:12].upper()
        
        return codigo_base
    
    def gerar_codigo_completo(self, regiao_id: int, codigo_base: str = None) -> str:
        """
        Gera código completo com identificador de região
        
        Args:
            regiao_id (int): Identificador da região (1, 2 ou 3)
            codigo_base (str, optional): Código base. Se não fornecido, será gerado
            
        Returns:
            str: Código completo com identificador de região
        """
        if not codigo_base:
            codigo_base = self.gerar_codigo_unico()
        
        # Valida região
        if regiao_id not in [1, 2, 3]:
            regiao_id = 1  # Default para Norte/Nordeste
        
        codigo_completo = f"{regiao_id}{codigo_base}"
        return codigo_completo
    
    def criar_imagem_codigo_barras(self, codigo: str) -> Tuple[BytesIO, Dict]:
        """
        Cria imagem do código de barras
        
        Args:
            codigo (str): Código para gerar o código de barras
            
        Returns:
            Tuple[BytesIO, Dict]: (buffer da imagem, metadados)
        """
        try:
            # Cria o código de barras
            codigo_barras_class = barcode.get_barcode_class(self.formato)
            codigo_barras = codigo_barras_class(codigo, writer=ImageWriter())
            
            # Configura opções da imagem
            opcoes = {
                'module_width': self.largura,
                'module_height': self.altura,
                'quiet_zone': 6.5,
                'font_size': 10,
                'text_distance': 5.0,
                'background': 'white',
                'foreground': 'black',
                'write_text': True,
                'text': codigo
            }
            
            # Gera a imagem em buffer
            buffer = BytesIO()
            codigo_barras.write(buffer, options=opcoes)
            buffer.seek(0)
            
            # Metadados da imagem
            metadados = {
                'formato': self.formato,
                'codigo': codigo,
                'largura': self.largura,
                'altura': self.altura,
                'tamanho_buffer': len(buffer.getvalue())
            }
            
            return buffer, metadados
            
        except Exception as e:
            raise Exception(f"Erro ao criar imagem do código de barras: {str(e)}")
    
    def salvar_imagem_arquivo(self, buffer: BytesIO, nome_arquivo: str) -> Tuple[str, int]:
        """
        Salva imagem do buffer em arquivo
        
        Args:
            buffer (BytesIO): Buffer da imagem
            nome_arquivo (str): Nome do arquivo (sem extensão)
            
        Returns:
            Tuple[str, int]: (caminho_completo, tamanho_arquivo)
        """
        try:
            # Garante extensão PNG
            if not nome_arquivo.endswith('.png'):
                nome_arquivo += '.png'
            
            caminho_completo = os.path.join(self.pasta_uploads, nome_arquivo)
            
            # Salva o arquivo
            with open(caminho_completo, 'wb') as arquivo:
                buffer.seek(0)
                conteudo = buffer.read()
                arquivo.write(conteudo)
                tamanho_arquivo = len(conteudo)
            
            return caminho_completo, tamanho_arquivo
            
        except Exception as e:
            raise Exception(f"Erro ao salvar arquivo: {str(e)}")
    
    def gerar_nome_arquivo(self, codigo: str, produto_id: int = None) -> str:
        """
        Gera nome único para o arquivo
        
        Args:
            codigo (str): Código do código de barras
            produto_id (int, optional): ID do produto
            
        Returns:
            str: Nome do arquivo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if produto_id:
            nome = f"barcode_{produto_id}_{codigo}_{timestamp}"
        else:
            nome = f"barcode_{codigo}_{timestamp}"
        
        return nome
    
    def criar_codigo_barras_completo(self, produto_id: int, regiao_id: int = None) -> Optional[CodigoBarras]:
        """
        Cria código de barras completo (registro no banco + arquivo)
        
        Args:
            produto_id (int): ID do produto
            regiao_id (int, optional): ID da região. Se não fornecido, será obtido do produto
            
        Returns:
            Optional[CodigoBarras]: Registro do código de barras criado
        """
        try:
            # Busca o produto
            produto = Produto.query.get(produto_id)
            if not produto:
                raise Exception(f"Produto com ID {produto_id} não encontrado")
            
            # Determina região
            if regiao_id is None:
                regiao_id = produto.regiao_id
            
            # Gera códigos
            codigo_base = self.gerar_codigo_unico()
            codigo_completo = self.gerar_codigo_completo(regiao_id, codigo_base)
            
            # Cria imagem
            buffer, metadados = self.criar_imagem_codigo_barras(codigo_completo)
            
            # Gera nome do arquivo
            nome_arquivo = self.gerar_nome_arquivo(codigo_completo, produto_id)
            
            # Salva arquivo
            caminho_arquivo, tamanho_arquivo = self.salvar_imagem_arquivo(buffer, nome_arquivo)
            
            # Cria registro no banco
            codigo_barras = CodigoBarras(
                codigo=codigo_base,
                codigo_completo=codigo_completo,
                regiao_identificador=regiao_id,
                formato=self.formato,
                produto_id=produto_id,
                nome_arquivo=nome_arquivo + '.png',
                caminho_arquivo=caminho_arquivo,
                tamanho_arquivo=tamanho_arquivo
            )
            
            db.session.add(codigo_barras)
            db.session.commit()
            
            return codigo_barras
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar código de barras completo: {e}")
            return None
    
    def buscar_codigo_barras(self, codigo_id: int) -> Optional[CodigoBarras]:
        """
        Busca código de barras por ID
        
        Args:
            codigo_id (int): ID do código de barras
            
        Returns:
            Optional[CodigoBarras]: Código de barras encontrado
        """
        return CodigoBarras.query.filter_by(id=codigo_id, ativo=True).first()
    
    def buscar_por_codigo_completo(self, codigo_completo: str) -> Optional[CodigoBarras]:
        """
        Busca código de barras pelo código completo
        
        Args:
            codigo_completo (str): Código completo
            
        Returns:
            Optional[CodigoBarras]: Código de barras encontrado
        """
        return CodigoBarras.query.filter_by(codigo_completo=codigo_completo, ativo=True).first()
    
    def listar_codigos_produto(self, produto_id: int) -> list:
        """
        Lista todos os códigos de barras de um produto
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            list: Lista de códigos de barras do produto
        """
        codigos = CodigoBarras.query.filter_by(
            produto_id=produto_id,
            ativo=True
        ).order_by(CodigoBarras.data_criacao.desc()).all()
        
        return [codigo.to_dict() for codigo in codigos]
    
    def registrar_download(self, codigo_id: int) -> bool:
        """
        Registra um download do código de barras
        
        Args:
            codigo_id (int): ID do código de barras
            
        Returns:
            bool: True se registrado com sucesso
        """
        try:
            codigo_barras = self.buscar_codigo_barras(codigo_id)
            if codigo_barras:
                codigo_barras.registrar_download()
                return True
            return False
        except Exception as e:
            print(f"Erro ao registrar download: {e}")
            return False
    
    def get_caminho_arquivo(self, codigo_id: int) -> Optional[str]:
        """
        Retorna caminho do arquivo do código de barras
        
        Args:
            codigo_id (int): ID do código de barras
            
        Returns:
            Optional[str]: Caminho do arquivo
        """
        codigo_barras = self.buscar_codigo_barras(codigo_id)
        if codigo_barras and codigo_barras.caminho_arquivo:
            if os.path.exists(codigo_barras.caminho_arquivo):
                return codigo_barras.caminho_arquivo
        return None
    
    def deletar_codigo_barras(self, codigo_id: int) -> bool:
        """
        Deleta código de barras (soft delete)
        
        Args:
            codigo_id (int): ID do código de barras
            
        Returns:
            bool: True se deletado com sucesso
        """
        try:
            codigo_barras = self.buscar_codigo_barras(codigo_id)
            if codigo_barras:
                codigo_barras.ativo = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar código de barras: {e}")
            return False
    
    def get_estatisticas(self) -> Dict:
        """
        Retorna estatísticas dos códigos de barras
        
        Returns:
            Dict: Estatísticas dos códigos de barras
        """
        try:
            from sqlalchemy import func
            
            # Total de códigos
            total_codigos = CodigoBarras.query.filter_by(ativo=True).count()
            
            # Códigos por região
            stats_regioes = db.session.query(
                CodigoBarras.regiao_identificador,
                func.count(CodigoBarras.id).label('total')
            ).filter_by(ativo=True).group_by(CodigoBarras.regiao_identificador).all()
            
            # Total de downloads
            total_downloads = db.session.query(
                func.sum(CodigoBarras.total_downloads)
            ).filter_by(ativo=True).scalar() or 0
            
            # Formata estatísticas por região
            regioes_stats = {}
            for stat in stats_regioes:
                regiao_id = stat.regiao_identificador
                from .region_service import RegionService
                region_service = RegionService()
                
                regioes_stats[regiao_id] = {
                    'nome': region_service.get_nome_regiao(regiao_id),
                    'total_codigos': stat.total
                }
            
            return {
                'total_codigos': total_codigos,
                'total_downloads': total_downloads,
                'codigos_por_regiao': regioes_stats,
                'formato_padrao': self.formato
            }
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {
                'total_codigos': 0,
                'total_downloads': 0,
                'codigos_por_regiao': {},
                'erro': str(e)
            }

