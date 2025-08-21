#!/usr/bin/env python3
"""Script de teste para verificar se as importações estão funcionando"""

try:
    print("Testando importações...")
    
    from main import create_app
    print("✅ create_app importado com sucesso")
    
    from app.models import db, Produto, CodigoBarras, CepRegiao
    print("✅ Modelos importados com sucesso")
    
    app = create_app('development')
    print("✅ App criado com sucesso")
    
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso")
    
    print("🎉 Todos os testes passaram!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

