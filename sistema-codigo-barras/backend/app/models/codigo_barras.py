from . import db
from datetime import datetime
import uuid

class CodigoBarras(db.Model):
    """Modelo para representar códigos de barras gerados"""
    
    __tablename__ = 'codigos_barras'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # Código único gerado
    codigo_completo = db.Column(db.String(100), nullable=False)  # Código com identificador de região
    regiao_identificador = db.Column(db.Integer, nullable=False)  # 1, 2 ou 3
    formato = db.Column(db.String(20), default='CODE128')  # Formato do código de barras
    
    # Relacionamento com produto
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    # Informações do arquivo gerado
    nome_arquivo = db.Column(db.String(200), nullable=True)  # Nome do arquivo PNG gerado
    caminho_arquivo = db.Column(db.String(500), nullable=True)  # Caminho completo do arquivo
    tamanho_arquivo = db.Column(db.Integer, nullable=True)  # Tamanho em bytes
    
    # Metadados
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_ultimo_download = db.Column(db.DateTime, nullable=True)
    total_downloads = db.Column(db.Integer, default=0)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<CodigoBarras {self.codigo_completo}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'codigo_completo': self.codigo_completo,
            'regiao_identificador': self.regiao_identificador,
            'formato': self.formato,
            'produto_id': self.produto_id,
            'nome_arquivo': self.nome_arquivo,
            'caminho_arquivo': self.caminho_arquivo,
            'tamanho_arquivo': self.tamanho_arquivo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_ultimo_download': self.data_ultimo_download.isoformat() if self.data_ultimo_download else None,
            'total_downloads': self.total_downloads,
            'ativo': self.ativo
        }
    
    @staticmethod
    def gerar_codigo_unico():
        """Gera um código único para o código de barras"""
        # Gera um UUID e pega os primeiros 12 caracteres
        codigo_base = str(uuid.uuid4()).replace('-', '')[:12].upper()
        return codigo_base
    
    def gerar_codigo_completo(self, regiao_id):
        """Gera o código completo com identificador de região"""
        if not self.codigo:
            self.codigo = self.gerar_codigo_unico()
        
        self.regiao_identificador = regiao_id
        self.codigo_completo = f"{regiao_id}{self.codigo}"
        return self.codigo_completo
    
    def registrar_download(self):
        """Registra um download do código de barras"""
        self.data_ultimo_download = datetime.utcnow()
        self.total_downloads += 1
        db.session.commit()
    
    def get_url_download(self):
        """Retorna a URL para download do arquivo"""
        if self.nome_arquivo:
            return f"/api/barcode/download/{self.id}"
        return None
    
    def get_regiao_nome(self):
        """Retorna o nome da região baseado no identificador"""
        regioes = {
            1: 'Norte/Nordeste',
            2: 'Centro-Oeste', 
            3: 'Sul/Sudeste'
        }
        return regioes.get(self.regiao_identificador, 'Desconhecida')

