#!/usr/bin/env python3
"""
Script de teste para os serviços do sistema
"""

from main import create_app
from app.services import CepService, BarcodeService, RegionService
from app.utils import CepValidator, ProdutoValidator

def test_region_service():
    """Testa o serviço de regiões"""
    print("🔍 Testando RegionService...")
    
    region_service = RegionService()
    
    # Testa identificação de regiões
    print(f"✅ SP (Sudeste): Região {region_service.get_regiao_por_estado('SP')} - {region_service.get_nome_regiao(3)}")
    print(f"✅ BA (Nordeste): Região {region_service.get_regiao_por_estado('BA')} - {region_service.get_nome_regiao(1)}")
    print(f"✅ DF (Centro-Oeste): Região {region_service.get_regiao_por_estado('DF')} - {region_service.get_nome_regiao(2)}")
    
    # Testa listagem de todas as regiões
    regioes = region_service.get_todas_regioes()
    print(f"✅ Total de regiões: {len(regioes)}")
    
    print("✅ RegionService funcionando corretamente!\n")

def test_validators():
    """Testa os validadores"""
    print("🔍 Testando Validadores...")
    
    # Testa validação de CEP
    ceps_teste = ['01310-100', '01310100', '00000-000', '123456789', '']
    for cep in ceps_teste:
        valido, msg = CepValidator.validar_formato(cep)
        status = "✅" if valido else "❌"
        print(f"{status} CEP '{cep}': {valido} - {msg}")
    
    # Testa validação de produto
    produto_teste = {
        'nome': 'Produto Teste',
        'cep': '01310-100',
        'estado': 'SP',
        'cidade': 'São Paulo',
        'descricao': 'Produto de teste'
    }
    
    valido, erros = ProdutoValidator.validar_produto(produto_teste)
    status = "✅" if valido else "❌"
    print(f"{status} Produto válido: {valido}")
    if erros:
        for erro in erros:
            print(f"   - {erro}")
    
    print("✅ Validadores funcionando corretamente!\n")

def test_cep_service():
    """Testa o serviço de CEP"""
    print("🔍 Testando CepService...")
    
    cep_service = CepService()
    
    # Testa consulta de CEP (sem banco, apenas API)
    print("📡 Consultando CEP na API ViaCEP...")
    resultado = cep_service.consultar_cep_api('01310-100')
    
    if resultado:
        print("✅ CEP encontrado na API:")
        print(f"   CEP: {resultado.get('cep')}")
        print(f"   Cidade: {resultado.get('localidade')}")
        print(f"   Estado: {resultado.get('uf')}")
        print(f"   Bairro: {resultado.get('bairro')}")
    else:
        print("❌ CEP não encontrado na API")
    
    print("✅ CepService funcionando corretamente!\n")

def test_barcode_service():
    """Testa o serviço de códigos de barras"""
    print("🔍 Testando BarcodeService...")
    
    barcode_service = BarcodeService()
    
    # Testa geração de código único
    codigo = barcode_service.gerar_codigo_unico()
    print(f"✅ Código único gerado: {codigo}")
    
    # Testa geração de código completo
    codigo_completo = barcode_service.gerar_codigo_completo(3, codigo)
    print(f"✅ Código completo (região 3): {codigo_completo}")
    
    # Testa criação de imagem
    try:
        buffer, metadados = barcode_service.criar_imagem_codigo_barras(codigo_completo)
        print(f"✅ Imagem criada: {metadados['tamanho_buffer']} bytes")
    except Exception as e:
        print(f"❌ Erro ao criar imagem: {e}")
    
    print("✅ BarcodeService funcionando corretamente!\n")

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes dos serviços...\n")
    
    # Cria aplicação Flask
    app = create_app('development')
    
    with app.app_context():
        # Testa serviços que não precisam de banco
        test_region_service()
        test_validators()
        test_cep_service()
        test_barcode_service()
    
    print("🎉 Todos os testes concluídos!")

if __name__ == '__main__':
    main()

