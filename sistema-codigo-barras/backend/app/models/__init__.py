from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância do SQLAlchemy
db = SQLAlchemy()

# Importar todos os modelos para garantir que sejam registrados
from .produto import Produto
from .codigo_barras import CodigoBarras
from .cep_regiao import CepRegiao

__all__ = ['db', 'Produto', 'CodigoBarras', 'CepRegiao']

