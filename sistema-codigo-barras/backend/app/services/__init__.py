"""
Módulo de serviços do Sistema de Códigos de Barras por CEP

Este módulo contém todos os serviços de negócio da aplicação:
- Serviços de consulta CEP
- Serviços de geração de códigos de barras
- Serviços de identificação de regiões
"""

from .cep_service import CepService
from .barcode_service import BarcodeService
from .region_service import RegionService

__all__ = ['CepService', 'BarcodeService', 'RegionService']

