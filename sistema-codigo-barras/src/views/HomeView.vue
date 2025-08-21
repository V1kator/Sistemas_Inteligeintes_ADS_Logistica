<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            Sistema de Códigos de Barras
            <span class="hero-subtitle">por CEP</span>
          </h1>
          <p class="hero-description">
            Gere e decodifique códigos de barras baseados em CEP brasileiro 
            com identificadores regionais automáticos
          </p>
          <div class="hero-actions">
            <router-link to="/scanner" class="btn btn-primary btn-large">
              <i class="icon">📷</i>
              Iniciar Scanner
            </router-link>
            <router-link to="/gerar" class="btn btn-secondary btn-large">
              <i class="icon">🏷️</i>
              Gerar Código
            </router-link>
          </div>
        </div>
        <div class="hero-visual">
          <div class="barcode-demo">
            <div class="barcode-lines">
              <span v-for="n in 20" :key="n" :style="{ height: Math.random() * 60 + 20 + 'px' }"></span>
            </div>
            <div class="barcode-text">3A1B2C3D4E5F6</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">Funcionalidades Principais</h2>
        <div class="features-grid">
          <div class="feature-card" @click="navigateTo('/scanner')">
            <div class="feature-icon scanner">📷</div>
            <h3>Scanner via Webcam</h3>
            <p>Decodifique códigos de barras em tempo real usando sua câmera</p>
            <div class="feature-stats">
              <span>✓ CODE 128</span>
              <span>✓ Tempo real</span>
            </div>
          </div>

          <div class="feature-card" @click="navigateTo('/gerar')">
            <div class="feature-icon generator">🏷️</div>
            <h3>Geração Automática</h3>
            <p>Crie códigos de barras com identificadores regionais baseados em CEP</p>
            <div class="feature-stats">
              <span>✓ 3 Regiões</span>
              <span>✓ Download PNG</span>
            </div>
          </div>

          <div class="feature-card" @click="navigateTo('/produtos')">
            <div class="feature-icon products">📦</div>
            <h3>Gestão de Produtos</h3>
            <p>Gerencie produtos e seus códigos de barras de forma organizada</p>
            <div class="feature-stats">
              <span>✓ CRUD Completo</span>
              <span>✓ Busca Avançada</span>
            </div>
          </div>

          <div class="feature-card" @click="navigateTo('/estatisticas')">
            <div class="feature-icon stats">📊</div>
            <h3>Estatísticas</h3>
            <p>Acompanhe métricas e relatórios detalhados do sistema</p>
            <div class="feature-stats">
              <span>✓ Dashboards</span>
              <span>✓ Relatórios</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Regions Section -->
    <section class="regions-section">
      <div class="container">
        <h2 class="section-title">Identificadores Regionais</h2>
        <p class="section-description">
          Cada código de barras recebe um identificador baseado na região do CEP
        </p>
        <div class="regions-grid">
          <div class="region-card region-1">
            <div class="region-number">1</div>
            <h3>Norte / Nordeste</h3>
            <div class="region-states">
              <span>AC</span> <span>AP</span> <span>AM</span> <span>PA</span>
              <span>RO</span> <span>RR</span> <span>TO</span> <span>AL</span>
              <span>BA</span> <span>CE</span> <span>MA</span> <span>PB</span>
              <span>PE</span> <span>PI</span> <span>RN</span> <span>SE</span>
            </div>
          </div>

          <div class="region-card region-2">
            <div class="region-number">2</div>
            <h3>Centro-Oeste</h3>
            <div class="region-states">
              <span>DF</span> <span>GO</span> <span>MT</span> <span>MS</span>
            </div>
          </div>

          <div class="region-card region-3">
            <div class="region-number">3</div>
            <h3>Sul / Sudeste</h3>
            <div class="region-states">
              <span>ES</span> <span>MG</span> <span>RJ</span> <span>SP</span>
              <span>PR</span> <span>RS</span> <span>SC</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section" v-if="systemStats">
      <div class="container">
        <h2 class="section-title">Estatísticas do Sistema</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">{{ systemStats.total_produtos || 0 }}</div>
            <div class="stat-label">Produtos Cadastrados</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ systemStats.total_codigos || 0 }}</div>
            <div class="stat-label">Códigos Gerados</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ systemStats.total_downloads || 0 }}</div>
            <div class="stat-label">Downloads Realizados</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ systemStats.total_ceps_cache || 0 }}</div>
            <div class="stat-label">CEPs em Cache</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>Pronto para começar?</h2>
          <p>Experimente todas as funcionalidades do sistema agora mesmo</p>
          <div class="cta-actions">
            <router-link to="/scanner" class="btn btn-primary btn-large">
              Começar Scanner
            </router-link>
            <router-link to="/sobre" class="btn btn-outline btn-large">
              Saiba Mais
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()
    const systemStats = ref(null)
    const loading = ref(false)

    const navigateTo = (path) => {
      router.push(path)
    }

    const loadSystemStats = async () => {
      try {
        loading.value = true
        const response = await fetch(`${process.env.VUE_APP_API_URL || 'http://localhost:5000/api'}/stats/`)
        
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            systemStats.value = data.data
          }
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadSystemStats()
    })

    return {
      systemStats,
      loading,
      navigateTo
    }
  }
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.1;
}

.hero-subtitle {
  display: block;
  font-size: 2.5rem;
  color: #ffd700;
  font-weight: 600;
}

.hero-description {
  font-size: 1.3rem;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.barcode-demo {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.barcode-lines {
  display: flex;
  gap: 2px;
  justify-content: center;
  align-items: end;
  height: 80px;
  margin-bottom: 15px;
}

.barcode-lines span {
  width: 3px;
  background: #333;
  animation: barcodeAnimation 3s ease-in-out infinite;
}

.barcode-lines span:nth-child(odd) {
  animation-delay: 0.1s;
}

.barcode-text {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: #333;
  font-size: 1.1rem;
}

@keyframes barcodeAnimation {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-large {
  padding: 16px 32px;
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
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-outline:hover {
  background: white;
  color: #667eea;
}

/* Sections */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
  font-weight: 700;
}

.section-description {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 50px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Features Section */
.features-section {
  padding: 80px 0;
  background: #f8f9fa;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  margin: 0 auto 20px;
}

.feature-icon.scanner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-icon.generator {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.feature-icon.products {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.feature-icon.stats {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.feature-card p {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

.feature-stats {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.feature-stats span {
  background: #e9ecef;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 14px;
  color: #495057;
  font-weight: 500;
}

/* Regions Section */
.regions-section {
  padding: 80px 0;
  background: white;
}

.regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.region-card {
  padding: 40px 30px;
  border-radius: 15px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.region-card.region-1 {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.region-card.region-2 {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.region-card.region-3 {
  background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
}

.region-number {
  font-size: 4rem;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 10px;
}

.region-card h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #2c3e50;
}

.region-states {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.region-states span {
  background: rgba(255, 255, 255, 0.8);
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

/* Stats Section */
.stats-section {
  padding: 80px 0;
  background: #2c3e50;
  color: white;
}

.stats-section .section-title {
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
}

.stat-card {
  text-align: center;
  padding: 30px 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* CTA Section */
.cta-section {
  padding: 80px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  font-weight: 700;
}

.cta-content p {
  font-size: 1.3rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.cta-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

/* Responsividade */
@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 2rem;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .features-grid,
  .regions-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>

