from . import db
from datetime import datetime

class Produto(db.Model):
    """Modelo para representar produtos no sistema"""
    
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    cep = db.Column(db.String(9), nullable=False)  # CEP no formato 00000-000
    cep_numerico = db.Column(db.String(8), nullable=False)  # CEP apenas números
    estado = db.Column(db.String(2), nullable=False)  # UF do estado
    cidade = db.Column(db.String(100), nullable=False)
    regiao_id = db.Column(db.Integer, nullable=False)  # 1, 2 ou 3
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com códigos de barras
    codigos_barras = db.relationship('CodigoBarras', backref='produto', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Produto {self.nome} - CEP: {self.cep}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'cep': self.cep,
            'cep_numerico': self.cep_numerico,
            'estado': self.estado,
            'cidade': self.cidade,
            'regiao_id': self.regiao_id,
            'regiao_nome': self.get_regiao_nome(),
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'ativo': self.ativo,
            'total_codigos': len(self.codigos_barras) if self.codigos_barras else 0
        }
    
    def get_regiao_nome(self):
        """Retorna o nome da região baseado no ID"""
        regioes = {
            1: 'Norte/Nordeste',
            2: 'Centro-Oeste',
            3: 'Sul/Sudeste'
        }
        return regioes.get(self.regiao_id, 'Desconhecida')
    
    @staticmethod
    def get_regiao_por_estado(uf):
        """Retorna o ID da região baseado na UF do estado"""
        from config import Config
        return Config.REGIOES_BRASIL.get(uf.upper(), 1)  # Default para Norte/Nordeste
    
    def atualizar_regiao(self):
        """Atualiza a região baseada no estado atual"""
        self.regiao_id = self.get_regiao_por_estado(self.estado)
        return self.regiao_id

