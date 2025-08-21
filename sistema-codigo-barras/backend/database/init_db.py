#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do Sistema de Códigos de Barras por CEP
"""

import os
import sys

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.models import db, Produto, CodigoBarras, CepRegiao

def init_database():
    """Inicializa o banco de dados criando todas as tabelas"""
    
    app = create_app('development')
    
    with app.app_context():
        print("🔧 Inicializando banco de dados...")
        
        # Remove todas as tabelas existentes (cuidado em produção!)
        db.drop_all()
        print("🗑️  Tabelas antigas removidas")
        
        # Cria todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso:")
        
        # Lista as tabelas criadas
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        for table in tables:
            print(f"   - {table}")
        
        print(f"\n💾 Banco de dados criado em: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("🎉 Inicialização concluída!")

def seed_sample_data():
    """Insere dados de exemplo para teste"""
    
    app = create_app('development')
    
    with app.app_context():
        print("🌱 Inserindo dados de exemplo...")
        
        # Dados de exemplo de CEPs
        ceps_exemplo = [
            {
                'cep': '01310-100',
                'cep_numerico': '01310100',
                'estado': 'SP',
                'cidade': 'São Paulo',
                'bairro': 'Bela Vista',
                'logradouro': 'Avenida Paulista',
                'regiao_id': 3,
                'regiao_nome': 'Sul/Sudeste'
            },
            {
                'cep': '70040-010',
                'cep_numerico': '70040010',
                'estado': 'DF',
                'cidade': 'Brasília',
                'bairro': 'Asa Norte',
                'logradouro': 'SBN Quadra 1',
                'regiao_id': 2,
                'regiao_nome': 'Centro-Oeste'
            },
            {
                'cep': '40070-110',
                'cep_numerico': '40070110',
                'estado': 'BA',
                'cidade': 'Salvador',
                'bairro': 'Pelourinho',
                'logradouro': 'Largo do Pelourinho',
                'regiao_id': 1,
                'regiao_nome': 'Norte/Nordeste'
            }
        ]
        
        # Insere CEPs de exemplo
        for cep_data in ceps_exemplo:
            cep_regiao = CepRegiao(**cep_data)
            db.session.add(cep_regiao)
        
        # Produtos de exemplo
        produtos_exemplo = [
            {
                'nome': 'Produto Teste SP',
                'descricao': 'Produto de teste para região Sudeste',
                'cep': '01310-100',
                'cep_numerico': '01310100',
                'estado': 'SP',
                'cidade': 'São Paulo',
                'regiao_id': 3
            },
            {
                'nome': 'Produto Teste DF',
                'descricao': 'Produto de teste para região Centro-Oeste',
                'cep': '70040-010',
                'cep_numerico': '70040010',
                'estado': 'DF',
                'cidade': 'Brasília',
                'regiao_id': 2
            }
        ]
        
        # Insere produtos de exemplo
        for produto_data in produtos_exemplo:
            produto = Produto(**produto_data)
            db.session.add(produto)
        
        # Salva no banco
        db.session.commit()
        
        print(f"✅ Inseridos {len(ceps_exemplo)} CEPs de exemplo")
        print(f"✅ Inseridos {len(produtos_exemplo)} produtos de exemplo")
        print("🎉 Dados de exemplo inseridos com sucesso!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Inicializa o banco de dados')
    parser.add_argument('--seed', action='store_true', 
                       help='Insere dados de exemplo após inicializar')
    
    args = parser.parse_args()
    
    # Inicializa o banco
    init_database()
    
    # Insere dados de exemplo se solicitado
    if args.seed:
        seed_sample_data()

