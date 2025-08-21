<template>
  <div class="scanner-view">
    <div class="container">
      <header class="page-header">
        <h1>Scanner de Códigos de Barras</h1>
        <p class="subtitle">
          Decodifique códigos de barras em tempo real usando sua webcam
        </p>
      </header>

      <main class="main-content">
        <!-- Componente do Scanner -->
        <BarcodeScanner />

        <!-- Seção de Informações -->
        <section class="info-section">
          <div class="info-grid">
            <div class="info-card">
              <div class="info-icon">
                <i class="icon-camera"></i>
              </div>
              <h3>Como Usar</h3>
              <ul>
                <li>Clique em "Iniciar Scanner"</li>
                <li>Permita acesso à câmera</li>
                <li>Aponte para um código de barras</li>
                <li>Aguarde a detecção automática</li>
              </ul>
            </div>

            <div class="info-card">
              <div class="info-icon">
                <i class="icon-barcode"></i>
              </div>
              <h3>Códigos Suportados</h3>
              <ul>
                <li>CODE 128 (principal)</li>
                <li>CODE 39</li>
                <li>EAN-13 / EAN-8</li>
                <li>UPC-A / UPC-E</li>
              </ul>
            </div>

            <div class="info-card">
              <div class="info-icon">
                <i class="icon-map"></i>
              </div>
              <h3>Regiões</h3>
              <ul>
                <li><strong>1:</strong> Norte/Nordeste</li>
                <li><strong>2:</strong> Centro-Oeste</li>
                <li><strong>3:</strong> Sul/Sudeste</li>
              </ul>
            </div>

            <div class="info-card">
              <div class="info-icon">
                <i class="icon-download"></i>
              </div>
              <h3>Funcionalidades</h3>
              <ul>
                <li>Detecção em tempo real</li>
                <li>Busca de produtos</li>
                <li>Download de códigos PNG</li>
                <li>Histórico de scans</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- Seção de Dicas -->
        <section class="tips-section">
          <h2>Dicas para Melhor Detecção</h2>
          <div class="tips-grid">
            <div class="tip-item">
              <i class="icon-light"></i>
              <div>
                <h4>Boa Iluminação</h4>
                <p>Use o scanner em ambiente bem iluminado para melhor precisão</p>
              </div>
            </div>

            <div class="tip-item">
              <i class="icon-focus"></i>
              <div>
                <h4>Foco Adequado</h4>
                <p>Mantenha o código de barras centralizado e em foco</p>
              </div>
            </div>

            <div class="tip-item">
              <i class="icon-distance"></i>
              <div>
                <h4>Distância Ideal</h4>
                <p>Posicione a câmera a 10-30cm do código de barras</p>
              </div>
            </div>

            <div class="tip-item">
              <i class="icon-stable"></i>
              <div>
                <h4>Estabilidade</h4>
                <p>Mantenha a câmera estável para evitar desfoque</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import BarcodeScanner from '../components/BarcodeScanner.vue'

export default {
  name: 'ScannerView',
  components: {
    BarcodeScanner
  },
  setup() {
    // Configurações da página
    document.title = 'Scanner de Códigos de Barras - Sistema CEP'
    
    return {}
  }
}
</script>

<style scoped>
.scanner-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin: 0;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.info-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
}

.info-card {
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  background: #f8f9fa;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.info-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: white;
  font-size: 24px;
}

.info-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.info-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-card li {
  padding: 5px 0;
  color: #555;
  font-size: 14px;
}

.tips-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.tips-section h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 2rem;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #007bff;
}

.tip-item i {
  font-size: 24px;
  color: #007bff;
  min-width: 30px;
}

.tip-item h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.tip-item p {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

/* Ícones personalizados usando CSS */
.icon-camera::before { content: "📷"; }
.icon-barcode::before { content: "📊"; }
.icon-map::before { content: "🗺️"; }
.icon-download::before { content: "💾"; }
.icon-light::before { content: "💡"; }
.icon-focus::before { content: "🎯"; }
.icon-distance::before { content: "📏"; }
.icon-stable::before { content: "⚖️"; }

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .info-grid,
  .tips-grid {
    grid-template-columns: 1fr;
  }
  
  .tip-item {
    flex-direction: column;
    text-align: center;
  }
  
  .container {
    padding: 0 15px;
  }
  
  .info-section,
  .tips-section {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .scanner-view {
    padding: 10px 0;
  }
  
  .page-header {
    margin-bottom: 20px;
  }
  
  .main-content {
    gap: 20px;
  }
}
</style>

