<template>
  <div class="not-found-view">
    <div class="container">
      <div class="not-found-content">
        <div class="error-visual">
          <div class="error-code">404</div>
          <div class="error-barcode">
            <div class="barcode-lines">
              <div class="line"></div>
              <div class="line"></div>
              <div class="line thick"></div>
              <div class="line"></div>
              <div class="line thick"></div>
              <div class="line"></div>
              <div class="line"></div>
              <div class="line thick"></div>
              <div class="line"></div>
              <div class="line"></div>
            </div>
            <div class="barcode-text">PÁGINA NÃO ENCONTRADA</div>
          </div>
        </div>
        
        <div class="error-message">
          <h1>Oops! Página não encontrada</h1>
          <p>
            A página que você está procurando não existe ou foi movida. 
            Que tal explorar outras funcionalidades do sistema?
          </p>
        </div>
        
        <div class="error-actions">
          <router-link to="/" class="btn btn-primary btn-large">
            <i class="icon">🏠</i>
            Voltar ao Início
          </router-link>
          
          <router-link to="/scanner" class="btn btn-secondary btn-large">
            <i class="icon">📷</i>
            Iniciar Scanner
          </router-link>
          
          <router-link to="/gerar" class="btn btn-outline btn-large">
            <i class="icon">🏷️</i>
            Gerar Código
          </router-link>
        </div>
        
        <div class="suggestions">
          <h3>Páginas populares:</h3>
          <div class="suggestions-grid">
            <router-link to="/" class="suggestion-card">
              <div class="suggestion-icon">🏠</div>
              <div class="suggestion-content">
                <h4>Página Inicial</h4>
                <p>Visão geral do sistema</p>
              </div>
            </router-link>
            
            <router-link to="/scanner" class="suggestion-card">
              <div class="suggestion-icon">📷</div>
              <div class="suggestion-content">
                <h4>Scanner</h4>
                <p>Decodificar códigos via webcam</p>
              </div>
            </router-link>
            
            <router-link to="/gerar" class="suggestion-card">
              <div class="suggestion-icon">🏷️</div>
              <div class="suggestion-content">
                <h4>Gerar Código</h4>
                <p>Criar novos códigos de barras</p>
              </div>
            </router-link>
            
            <router-link to="/produtos" class="suggestion-card">
              <div class="suggestion-icon">📦</div>
              <div class="suggestion-content">
                <h4>Produtos</h4>
                <p>Gerenciar produtos cadastrados</p>
              </div>
            </router-link>
            
            <router-link to="/estatisticas" class="suggestion-card">
              <div class="suggestion-icon">📊</div>
              <div class="suggestion-content">
                <h4>Estatísticas</h4>
                <p>Métricas e relatórios</p>
              </div>
            </router-link>
            
            <router-link to="/sobre" class="suggestion-card">
              <div class="suggestion-icon">ℹ️</div>
              <div class="suggestion-content">
                <h4>Sobre</h4>
                <p>Informações do sistema</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.not-found-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.not-found-content {
  background: white;
  border-radius: 20px;
  padding: 60px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
}

/* Visual do Erro */
.error-visual {
  margin-bottom: 40px;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  color: #e74c3c;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.error-barcode {
  display: inline-block;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 2px dashed #dee2e6;
}

.barcode-lines {
  display: flex;
  align-items: end;
  gap: 3px;
  margin-bottom: 10px;
  justify-content: center;
}

.line {
  width: 4px;
  height: 40px;
  background: #2c3e50;
  animation: barcodeAnimation 3s infinite;
}

.line.thick {
  width: 8px;
  height: 50px;
}

.line:nth-child(1) { animation-delay: 0.1s; }
.line:nth-child(2) { animation-delay: 0.2s; }
.line:nth-child(3) { animation-delay: 0.3s; }
.line:nth-child(4) { animation-delay: 0.4s; }
.line:nth-child(5) { animation-delay: 0.5s; }
.line:nth-child(6) { animation-delay: 0.6s; }
.line:nth-child(7) { animation-delay: 0.7s; }
.line:nth-child(8) { animation-delay: 0.8s; }
.line:nth-child(9) { animation-delay: 0.9s; }
.line:nth-child(10) { animation-delay: 1s; }

@keyframes barcodeAnimation {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.barcode-text {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  font-weight: bold;
  color: #666;
  letter-spacing: 2px;
}

/* Mensagem de Erro */
.error-message {
  margin-bottom: 40px;
}

.error-message h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
}

.error-message p {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* Ações */
.error-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 50px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border: none;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-large {
  padding: 18px 36px;
  font-size: 18px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.3);
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
}

.icon {
  font-size: 1.2em;
}

/* Sugestões */
.suggestions {
  text-align: left;
}

.suggestions h3 {
  color: #2c3e50;
  margin-bottom: 25px;
  text-align: center;
  font-size: 1.5rem;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.suggestion-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.suggestion-card:hover {
  background: #e9ecef;
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.15);
}

.suggestion-icon {
  font-size: 2.5rem;
  width: 60px;
  text-align: center;
}

.suggestion-content h4 {
  color: #2c3e50;
  margin-bottom: 5px;
  font-size: 1.1rem;
}

.suggestion-content p {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .not-found-content {
    padding: 40px 20px;
  }
  
  .error-code {
    font-size: 6rem;
  }
  
  .error-message h1 {
    font-size: 2rem;
  }
  
  .error-message p {
    font-size: 1.1rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
  
  .suggestions-grid {
    grid-template-columns: 1fr;
  }
  
  .barcode-lines {
    gap: 2px;
  }
  
  .line {
    width: 3px;
    height: 30px;
  }
  
  .line.thick {
    width: 6px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  .not-found-content {
    padding: 30px 15px;
  }
  
  .error-code {
    font-size: 4rem;
  }
  
  .error-message h1 {
    font-size: 1.8rem;
  }
  
  .suggestion-card {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .suggestion-icon {
    font-size: 2rem;
  }
}

/* Animações adicionais */
.not-found-content {
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.suggestion-card {
  animation: fadeInUp 0.8s ease-out;
}

.suggestion-card:nth-child(1) { animation-delay: 0.1s; }
.suggestion-card:nth-child(2) { animation-delay: 0.2s; }
.suggestion-card:nth-child(3) { animation-delay: 0.3s; }
.suggestion-card:nth-child(4) { animation-delay: 0.4s; }
.suggestion-card:nth-child(5) { animation-delay: 0.5s; }
.suggestion-card:nth-child(6) { animation-delay: 0.6s; }
</style>

