from . import db
from datetime import datetime

class CepRegiao(db.Model):
    """Modelo para mapear CEPs para regiões brasileiras"""
    
    __tablename__ = 'cep_regioes'
    
    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(9), nullable=False, index=True)  # CEP no formato 00000-000
    cep_numerico = db.Column(db.String(8), nullable=False, index=True)  # CEP apenas números
    estado = db.Column(db.String(2), nullable=False, index=True)  # UF do estado
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=True)
    logradouro = db.Column(db.String(200), nullable=True)
    regiao_id = db.Column(db.Integer, nullable=False, index=True)  # 1, 2 ou 3
    regiao_nome = db.Column(db.String(50), nullable=False)
    
    # Metadados
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fonte_dados = db.Column(db.String(50), default='ViaCEP')  # Fonte da informação
    ativo = db.Column(db.Boolean, default=True)
    
    # Índices compostos para otimizar consultas
    __table_args__ = (
        db.Index('idx_cep_numerico_ativo', 'cep_numerico', 'ativo'),
        db.Index('idx_estado_regiao', 'estado', 'regiao_id'),
    )
    
    def __repr__(self):
        return f'<CepRegiao {self.cep} - {self.cidade}/{self.estado}>'
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'cep': self.cep,
            'cep_numerico': self.cep_numerico,
            'estado': self.estado,
            'cidade': self.cidade,
            'bairro': self.bairro,
            'logradouro': self.logradouro,
            'regiao_id': self.regiao_id,
            'regiao_nome': self.regiao_nome,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'fonte_dados': self.fonte_dados,
            'ativo': self.ativo
        }
    
    @staticmethod
    def buscar_por_cep(cep):
        """Busca informações de região por CEP"""
        # Remove formatação do CEP
        cep_limpo = cep.replace('-', '').replace('.', '').strip()
        
        return CepRegiao.query.filter_by(
            cep_numerico=cep_limpo,
            ativo=True
        ).first()
    
    @staticmethod
    def criar_de_dados_cep(dados_cep):
        """Cria um registro a partir de dados de API de CEP"""
        from config import Config
        
        # Determina a região baseada no estado
        estado = dados_cep.get('uf', '').upper()
        regiao_id = Config.REGIOES_BRASIL.get(estado, 1)
        
        # Mapeia nomes das regiões
        regioes_nomes = {
            1: 'Norte/Nordeste',
            2: 'Centro-Oeste',
            3: 'Sul/Sudeste'
        }
        
        cep_formatado = dados_cep.get('cep', '')
        cep_numerico = cep_formatado.replace('-', '')
        
        cep_regiao = CepRegiao(
            cep=cep_formatado,
            cep_numerico=cep_numerico,
            estado=estado,
            cidade=dados_cep.get('localidade', ''),
            bairro=dados_cep.get('bairro', ''),
            logradouro=dados_cep.get('logradouro', ''),
            regiao_id=regiao_id,
            regiao_nome=regioes_nomes.get(regiao_id, 'Desconhecida'),
            fonte_dados='ViaCEP'
        )
        
        return cep_regiao
    
    @staticmethod
    def get_estatisticas_regioes():
        """Retorna estatísticas de CEPs por região"""
        from sqlalchemy import func
        
        stats = db.session.query(
            CepRegiao.regiao_id,
            CepRegiao.regiao_nome,
            func.count(CepRegiao.id).label('total_ceps')
        ).filter_by(ativo=True).group_by(
            CepRegiao.regiao_id,
            CepRegiao.regiao_nome
        ).all()
        
        return [
            {
                'regiao_id': stat.regiao_id,
                'regiao_nome': stat.regiao_nome,
                'total_ceps': stat.total_ceps
            }
            for stat in stats
        ]

