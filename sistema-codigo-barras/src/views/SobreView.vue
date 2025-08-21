<template>
  <div class="sobre-view">
    <div class="container">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <h1>Sobre o Sistema</h1>
          <p class="hero-description">
            Sistema web completo para geração e decodificação de códigos de barras 
            baseado em CEP brasileiro com identificadores regionais automáticos
          </p>
        </div>
        <div class="hero-visual">
          <div class="tech-stack">
            <div class="tech-item">
              <div class="tech-icon">🐍</div>
              <span>Python</span>
            </div>
            <div class="tech-item">
              <div class="tech-icon">🌶️</div>
              <span>Flask</span>
            </div>
            <div class="tech-item">
              <div class="tech-icon">💚</div>
              <span>Vue.js</span>
            </div>
            <div class="tech-item">
              <div class="tech-icon">📷</div>
              <span>QuaggaJS</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Funcionalidades -->
      <section class="features-section">
        <h2>Funcionalidades Principais</h2>
        
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon scanner">📷</div>
            <h3>Scanner via Webcam</h3>
            <p>Decodificação de códigos de barras em tempo real usando a câmera do dispositivo com tecnologia QuaggaJS.</p>
            <ul>
              <li>Suporte a formato CODE 128</li>
              <li>Detecção automática em tempo real</li>
              <li>Interface responsiva e intuitiva</li>
              <li>Compatível com desktop e mobile</li>
            </ul>
          </div>

          <div class="feature-item">
            <div class="feature-icon generator">🏷️</div>
            <h3>Geração Automática</h3>
            <p>Criação de códigos de barras únicos com identificadores regionais baseados no CEP do produto.</p>
            <ul>
              <li>3 identificadores regionais distintos</li>
              <li>Códigos únicos de 13 caracteres</li>
              <li>Download em formato PNG</li>
              <li>Integração com API ViaCEP</li>
            </ul>
          </div>

          <div class="feature-item">
            <div class="feature-icon management">📦</div>
            <h3>Gestão de Produtos</h3>
            <p>Sistema completo de CRUD para gerenciamento de produtos e seus códigos de barras associados.</p>
            <ul>
              <li>Cadastro completo de produtos</li>
              <li>Busca e filtros avançados</li>
              <li>Histórico de códigos gerados</li>
              <li>Estatísticas detalhadas</li>
            </ul>
          </div>

          <div class="feature-item">
            <div class="feature-icon regions">🗺️</div>
            <h3>Identificadores Regionais</h3>
            <p>Sistema inteligente de identificação regional baseado na localização geográfica do CEP.</p>
            <ul>
              <li>Região 1: Norte e Nordeste</li>
              <li>Região 2: Centro-Oeste</li>
              <li>Região 3: Sul e Sudeste</li>
              <li>Mapeamento automático por estado</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Tecnologias -->
      <section class="tech-section">
        <h2>Tecnologias Utilizadas</h2>
        
        <div class="tech-categories">
          <div class="tech-category">
            <h3>Backend</h3>
            <div class="tech-list">
              <div class="tech-detail">
                <div class="tech-logo">🐍</div>
                <div class="tech-info">
                  <h4>Python 3.11</h4>
                  <p>Linguagem principal do backend com foco em simplicidade e produtividade</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">🌶️</div>
                <div class="tech-info">
                  <h4>Flask 3.1</h4>
                  <p>Framework web minimalista e flexível para criação de APIs REST</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">🗄️</div>
                <div class="tech-info">
                  <h4>SQLAlchemy</h4>
                  <p>ORM poderoso para gerenciamento de banco de dados relacional</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">📊</div>
                <div class="tech-info">
                  <h4>python-barcode</h4>
                  <p>Biblioteca para geração de códigos de barras em diversos formatos</p>
                </div>
              </div>
            </div>
          </div>

          <div class="tech-category">
            <h3>Frontend</h3>
            <div class="tech-list">
              <div class="tech-detail">
                <div class="tech-logo">💚</div>
                <div class="tech-info">
                  <h4>Vue.js 3</h4>
                  <p>Framework progressivo para construção de interfaces de usuário modernas</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">🛣️</div>
                <div class="tech-info">
                  <h4>Vue Router</h4>
                  <p>Roteamento oficial do Vue.js para navegação entre páginas</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">📷</div>
                <div class="tech-info">
                  <h4>QuaggaJS</h4>
                  <p>Biblioteca JavaScript para leitura de códigos de barras via webcam</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">🎨</div>
                <div class="tech-info">
                  <h4>CSS3 Moderno</h4>
                  <p>Estilos responsivos com Grid, Flexbox e animações CSS</p>
                </div>
              </div>
            </div>
          </div>

          <div class="tech-category">
            <h3>Banco de Dados</h3>
            <div class="tech-list">
              <div class="tech-detail">
                <div class="tech-logo">💾</div>
                <div class="tech-info">
                  <h4>SQLite</h4>
                  <p>Banco de dados leve e eficiente para desenvolvimento e produção</p>
                </div>
              </div>
              
              <div class="tech-detail">
                <div class="tech-logo">🔗</div>
                <div class="tech-info">
                  <h4>API ViaCEP</h4>
                  <p>Integração com serviço externo para consulta de CEPs brasileiros</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Arquitetura -->
      <section class="architecture-section">
        <h2>Arquitetura do Sistema</h2>
        
        <div class="architecture-diagram">
          <div class="layer frontend-layer">
            <h3>Frontend (Vue.js)</h3>
            <div class="layer-components">
              <div class="component">Interface de Usuário</div>
              <div class="component">Scanner de Códigos</div>
              <div class="component">Gestão de Produtos</div>
              <div class="component">Geração de Códigos</div>
            </div>
          </div>
          
          <div class="connection">
            <div class="arrow">↕️</div>
            <span>API REST</span>
          </div>
          
          <div class="layer backend-layer">
            <h3>Backend (Flask)</h3>
            <div class="layer-components">
              <div class="component">Rotas da API</div>
              <div class="component">Serviços de Negócio</div>
              <div class="component">Validadores</div>
              <div class="component">Modelos de Dados</div>
            </div>
          </div>
          
          <div class="connection">
            <div class="arrow">↕️</div>
            <span>ORM</span>
          </div>
          
          <div class="layer database-layer">
            <h3>Banco de Dados (SQLite)</h3>
            <div class="layer-components">
              <div class="component">Produtos</div>
              <div class="component">Códigos de Barras</div>
              <div class="component">Cache de CEPs</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Estatísticas do Sistema -->
      <section class="stats-section" v-if="systemStats">
        <h2>Estatísticas do Sistema</h2>
        
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStats.total_produtos || 0 }}</div>
              <div class="stat-label">Produtos Cadastrados</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">🏷️</div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStats.total_codigos || 0 }}</div>
              <div class="stat-label">Códigos Gerados</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">💾</div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStats.total_downloads || 0 }}</div>
              <div class="stat-label">Downloads Realizados</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">🗺️</div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStats.total_ceps_cache || 0 }}</div>
              <div class="stat-label">CEPs em Cache</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Desenvolvimento -->
      <section class="development-section">
        <h2>Processo de Desenvolvimento</h2>
        
        <div class="development-timeline">
          <div class="timeline-item">
            <div class="timeline-marker">1</div>
            <div class="timeline-content">
              <h3>Configuração e Estrutura</h3>
              <p>Definição da arquitetura do projeto e organização de pastas</p>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker">2</div>
            <div class="timeline-content">
              <h3>Backend e APIs</h3>
              <p>Desenvolvimento do backend Flask com APIs REST completas</p>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker">3</div>
            <div class="timeline-content">
              <h3>Serviços e Integrações</h3>
              <p>Implementação dos serviços de CEP, códigos de barras e regiões</p>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker">4</div>
            <div class="timeline-content">
              <h3>Webcam e Decodificação</h3>
              <p>Integração do QuaggaJS para scanner via webcam</p>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker">5</div>
            <div class="timeline-content">
              <h3>Frontend Vue.js</h3>
              <p>Desenvolvimento da interface de usuário moderna e responsiva</p>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="timeline-marker">6</div>
            <div class="timeline-content">
              <h3>Testes e Integração</h3>
              <p>Testes completos e integração final de todos os componentes</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Contato e Links -->
      <section class="contact-section">
        <h2>Informações Adicionais</h2>
        
        <div class="contact-grid">
          <div class="contact-card">
            <h3>🚀 Funcionalidades</h3>
            <ul>
              <li>Scanner de códigos via webcam</li>
              <li>Geração automática de códigos</li>
              <li>Gestão completa de produtos</li>
              <li>Identificadores regionais</li>
              <li>Download de códigos em PNG</li>
              <li>Estatísticas detalhadas</li>
            </ul>
          </div>
          
          <div class="contact-card">
            <h3>🛠️ Tecnologias</h3>
            <ul>
              <li>Python 3.11 + Flask</li>
              <li>Vue.js 3 + Vue Router</li>
              <li>SQLAlchemy + SQLite</li>
              <li>QuaggaJS para scanner</li>
              <li>API ViaCEP</li>
              <li>CSS3 moderno</li>
            </ul>
          </div>
          
          <div class="contact-card">
            <h3>📊 Características</h3>
            <ul>
              <li>Interface responsiva</li>
              <li>API REST completa</li>
              <li>Validação de dados</li>
              <li>Cache inteligente</li>
              <li>Tratamento de erros</li>
              <li>Performance otimizada</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="cta-section">
        <div class="cta-content">
          <h2>Experimente o Sistema</h2>
          <p>Teste todas as funcionalidades e veja como é fácil gerenciar códigos de barras</p>
          <div class="cta-actions">
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
      </section>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'SobreView',
  setup() {
    const systemStats = ref(null)
    const loading = ref(false)

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
      loading
    }
  }
}
</script>

<style scoped>
.sobre-view {
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 60px;
  align-items: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  color: white;
}

.hero-description {
  font-size: 1.3rem;
  opacity: 0.9;
  line-height: 1.6;
  margin: 0;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.tech-item {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.tech-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.tech-item span {
  font-weight: 600;
  font-size: 1.1rem;
}

/* Sections */
section {
  padding: 80px 0;
}

section h2 {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 50px;
  color: #2c3e50;
}

/* Features */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-item {
  background: white;
  padding: 40px 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
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

.feature-icon.management {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.feature-icon.regions {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.feature-item h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.feature-item p {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

.feature-item ul {
  text-align: left;
  color: #666;
}

.feature-item li {
  margin-bottom: 8px;
}

/* Tecnologias */
.tech-section {
  background: white;
}

.tech-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
}

.tech-category h3 {
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 1.8rem;
  text-align: center;
}

.tech-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.tech-detail {
  display: flex;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.tech-detail:hover {
  transform: translateY(-5px);
}

.tech-logo {
  font-size: 2.5rem;
  width: 60px;
  text-align: center;
}

.tech-info h4 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.tech-info p {
  color: #666;
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}

/* Arquitetura */
.architecture-section {
  background: #f8f9fa;
}

.architecture-diagram {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.layer {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.layer h3 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.layer-components {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.component {
  background: #e9ecef;
  padding: 15px;
  border-radius: 8px;
  font-weight: 600;
  color: #495057;
}

.frontend-layer .component {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.backend-layer .component {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: white;
}

.database-layer .component {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
}

.connection {
  text-align: center;
  color: #666;
  font-weight: 600;
}

.arrow {
  font-size: 1.5rem;
  margin-bottom: 5px;
}

/* Estatísticas */
.stats-section {
  background: #2c3e50;
  color: white;
}

.stats-section h2 {
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 30px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  font-size: 3rem;
  width: 80px;
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* Timeline */
.development-section {
  background: white;
}

.development-timeline {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.development-timeline::before {
  content: '';
  position: absolute;
  left: 30px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #007bff;
}

.timeline-item {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  position: relative;
}

.timeline-marker {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.2rem;
  flex-shrink: 0;
  z-index: 1;
}

.timeline-content {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  flex: 1;
}

.timeline-content h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.timeline-content p {
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* Contato */
.contact-section {
  background: #f8f9fa;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.contact-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.contact-card h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.contact-card ul {
  list-style: none;
  padding: 0;
}

.contact-card li {
  padding: 8px 0;
  border-bottom: 1px solid #e9ecef;
  color: #666;
}

.contact-card li:last-child {
  border-bottom: none;
}

/* CTA */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-content h2 {
  color: white;
  margin-bottom: 20px;
}

.cta-content p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 40px;
}

.cta-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-2px);
}

/* Responsividade */
@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 60px 0;
  }
  
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .tech-stack {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-categories {
    grid-template-columns: 1fr;
  }
  
  .architecture-diagram {
    padding: 0 20px;
  }
  
  .layer-components {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .development-timeline::before {
    left: 15px;
  }
  
  .timeline-marker {
    width: 30px;
    height: 30px;
    font-size: 14px;
  }
  
  .timeline-item {
    gap: 20px;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
  
  section {
    padding: 60px 0;
  }
  
  section h2 {
    font-size: 2rem;
  }
}
</style>

