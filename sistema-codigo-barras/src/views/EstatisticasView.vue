<template>
  <div class="estatisticas-view">
    <div class="container">
      <!-- Header -->
      <header class="page-header">
        <div class="header-content">
          <h1>Estatísticas do Sistema</h1>
          <p class="subtitle">Acompanhe métricas e relatórios detalhados</p>
        </div>
        <div class="header-actions">
          <button @click="loadStats" class="btn btn-outline" :disabled="loading">
            <i class="icon">🔄</i>
            {{ loading ? 'Carregando...' : 'Atualizar' }}
          </button>
        </div>
      </header>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Carregando estatísticas...</p>
      </div>

      <div v-else-if="!stats" class="error-state">
        <h3>Erro ao carregar estatísticas</h3>
        <p>Não foi possível carregar os dados. Tente novamente.</p>
        <button @click="loadStats" class="btn btn-primary">
          Tentar Novamente
        </button>
      </div>

      <div v-else>
        <!-- Estatísticas Gerais -->
        <section class="general-stats">
          <h2>Visão Geral</h2>
          <div class="stats-grid">
            <div class="stat-card primary">
              <div class="stat-icon">📦</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.total_produtos || 0 }}</div>
                <div class="stat-label">Produtos Cadastrados</div>
                <div class="stat-change" v-if="stats.produtos_mes">
                  +{{ stats.produtos_mes }} este mês
                </div>
              </div>
            </div>

            <div class="stat-card success">
              <div class="stat-icon">🏷️</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.total_codigos || 0 }}</div>
                <div class="stat-label">Códigos Gerados</div>
                <div class="stat-change" v-if="stats.codigos_mes">
                  +{{ stats.codigos_mes }} este mês
                </div>
              </div>
            </div>

            <div class="stat-card warning">
              <div class="stat-icon">💾</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.total_downloads || 0 }}</div>
                <div class="stat-label">Downloads Realizados</div>
                <div class="stat-change" v-if="stats.downloads_mes">
                  +{{ stats.downloads_mes }} este mês
                </div>
              </div>
            </div>

            <div class="stat-card info">
              <div class="stat-icon">🗺️</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.total_ceps_cache || 0 }}</div>
                <div class="stat-label">CEPs em Cache</div>
                <div class="stat-change" v-if="stats.cache_hit_rate">
                  {{ (stats.cache_hit_rate * 100).toFixed(1) }}% hit rate
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Estatísticas por Região -->
        <section class="region-stats">
          <h2>Distribuição por Região</h2>
          <div class="regions-grid">
            <div 
              v-for="region in stats.stats_por_regiao || []" 
              :key="region.regiao_id"
              class="region-card"
              :class="`region-${region.regiao_id}`"
            >
              <div class="region-header">
                <div class="region-number">{{ region.regiao_id }}</div>
                <div class="region-name">{{ getRegionName(region.regiao_id) }}</div>
              </div>
              
              <div class="region-stats-content">
                <div class="region-stat">
                  <span class="stat-value">{{ region.total_produtos || 0 }}</span>
                  <span class="stat-label">Produtos</span>
                </div>
                <div class="region-stat">
                  <span class="stat-value">{{ region.total_codigos || 0 }}</span>
                  <span class="stat-label">Códigos</span>
                </div>
                <div class="region-stat">
                  <span class="stat-value">{{ region.total_downloads || 0 }}</span>
                  <span class="stat-label">Downloads</span>
                </div>
              </div>
              
              <div class="region-percentage">
                {{ ((region.total_produtos / (stats.total_produtos || 1)) * 100).toFixed(1) }}% do total
              </div>
            </div>
          </div>
        </section>

        <!-- Top Estados -->
        <section class="states-stats">
          <h2>Estados com Mais Produtos</h2>
          <div class="states-grid">
            <div 
              v-for="(estado, index) in stats.top_estados || []" 
              :key="estado.estado"
              class="state-card"
            >
              <div class="state-rank">{{ index + 1 }}º</div>
              <div class="state-content">
                <div class="state-name">{{ estado.estado }}</div>
                <div class="state-stats">
                  <span>{{ estado.total_produtos }} produtos</span>
                  <span>{{ estado.total_codigos }} códigos</span>
                </div>
              </div>
              <div class="state-percentage">
                {{ ((estado.total_produtos / (stats.total_produtos || 1)) * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
        </section>

        <!-- Atividade Recente -->
        <section class="activity-stats">
          <h2>Atividade Recente</h2>
          <div class="activity-grid">
            <div class="activity-card">
              <h3>📈 Crescimento</h3>
              <div class="activity-content">
                <div class="activity-item">
                  <span class="label">Produtos (30 dias):</span>
                  <span class="value growth">+{{ stats.crescimento_produtos_30d || 0 }}</span>
                </div>
                <div class="activity-item">
                  <span class="label">Códigos (30 dias):</span>
                  <span class="value growth">+{{ stats.crescimento_codigos_30d || 0 }}</span>
                </div>
                <div class="activity-item">
                  <span class="label">Downloads (30 dias):</span>
                  <span class="value growth">+{{ stats.crescimento_downloads_30d || 0 }}</span>
                </div>
              </div>
            </div>

            <div class="activity-card">
              <h3>⚡ Performance</h3>
              <div class="activity-content">
                <div class="activity-item">
                  <span class="label">Média códigos/produto:</span>
                  <span class="value">{{ (stats.media_codigos_por_produto || 0).toFixed(1) }}</span>
                </div>
                <div class="activity-item">
                  <span class="label">Média downloads/código:</span>
                  <span class="value">{{ (stats.media_downloads_por_codigo || 0).toFixed(1) }}</span>
                </div>
                <div class="activity-item">
                  <span class="label">Taxa de uso:</span>
                  <span class="value">{{ ((stats.produtos_com_codigos / (stats.total_produtos || 1)) * 100).toFixed(1) }}%</span>
                </div>
              </div>
            </div>

            <div class="activity-card">
              <h3>🕒 Últimas Atividades</h3>
              <div class="activity-content">
                <div class="activity-item">
                  <span class="label">Último produto:</span>
                  <span class="value">{{ formatDate(stats.ultimo_produto_criado) }}</span>
                </div>
                <div class="activity-item">
                  <span class="label">Último código:</span>
                  <span class="value">{{ formatDate(stats.ultimo_codigo_gerado) }}</span>
                </div>
                <div class="activity-item">
                  <span class="label">Último download:</span>
                  <span class="value">{{ formatDate(stats.ultimo_download) }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Informações do Sistema -->
        <section class="system-info">
          <h2>Informações do Sistema</h2>
          <div class="system-grid">
            <div class="system-card">
              <h3>🔧 Versão</h3>
              <div class="system-content">
                <div class="system-item">
                  <span class="label">Sistema:</span>
                  <span class="value">{{ stats.sistema?.versao || 'v1.0.0' }}</span>
                </div>
                <div class="system-item">
                  <span class="label">Ambiente:</span>
                  <span class="value">{{ stats.sistema?.ambiente || 'desenvolvimento' }}</span>
                </div>
              </div>
            </div>

            <div class="system-card">
              <h3>💾 Banco de Dados</h3>
              <div class="system-content">
                <div class="system-item">
                  <span class="label">Tipo:</span>
                  <span class="value">{{ stats.banco_dados?.tipo || 'SQLite' }}</span>
                </div>
                <div class="system-item">
                  <span class="label">Tamanho:</span>
                  <span class="value">{{ stats.banco_dados?.tamanho_formatado || '0 KB' }}</span>
                </div>
              </div>
            </div>

            <div class="system-card">
              <h3>⚙️ Configurações</h3>
              <div class="system-content">
                <div class="system-item">
                  <span class="label">Timeout API:</span>
                  <span class="value">{{ stats.configuracoes?.timeout_api || 10 }}s</span>
                </div>
                <div class="system-item">
                  <span class="label">Limite req/min:</span>
                  <span class="value">{{ stats.configuracoes?.limite_requisicoes || 60 }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Última Atualização -->
        <section class="update-info">
          <div class="update-card">
            <div class="update-content">
              <span class="update-label">Última atualização:</span>
              <span class="update-time">{{ formatDateTime(stats.data_consulta) }}</span>
            </div>
            <button @click="loadStats" class="btn btn-primary btn-sm">
              Atualizar Agora
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'EstatisticasView',
  setup() {
    const loading = ref(true)
    const stats = ref(null)

    const loadStats = async () => {
      try {
        loading.value = true
        const response = await fetch(`${process.env.VUE_APP_API_URL || 'http://localhost:5000/api'}/stats/`)
        
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            stats.value = data.data
          } else {
            stats.value = null
          }
        } else {
          stats.value = null
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
        stats.value = null
      } finally {
        loading.value = false
      }
    }

    const getRegionName = (regionId) => {
      const regions = {
        1: 'Norte/Nordeste',
        2: 'Centro-Oeste',
        3: 'Sul/Sudeste'
      }
      return regions[regionId] || 'Desconhecida'
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('pt-BR')
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString('pt-BR')
    }

    onMounted(() => {
      loadStats()
    })

    return {
      loading,
      stats,
      loadStats,
      getRegionName,
      formatDate,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.estatisticas-view {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.header-content h1 {
  font-size: 2.5rem;
  margin-bottom: 5px;
  color: white;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

/* Estados de Loading e Erro */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #666;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.error-state h3 {
  color: #dc3545;
  margin-bottom: 15px;
}

/* Seções */
section {
  margin-bottom: 40px;
}

section h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 25px;
  text-align: center;
}

/* Estatísticas Gerais */
.general-stats {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
}

.stat-card {
  padding: 25px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.stat-card.success {
  background: linear-gradient(135deg, #56ab2f, #a8e6cf);
  color: white;
}

.stat-card.warning {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: white;
}

.stat-card.info {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
}

.stat-icon {
  font-size: 3rem;
  opacity: 0.8;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 5px;
}

.stat-change {
  font-size: 0.85rem;
  opacity: 0.8;
}

/* Regiões */
.region-stats {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.region-card {
  padding: 25px;
  border-radius: 12px;
  color: white;
  position: relative;
  overflow: hidden;
}

.region-card.region-1 {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.region-card.region-2 {
  background: linear-gradient(135deg, #f39c12, #e67e22);
}

.region-card.region-3 {
  background: linear-gradient(135deg, #27ae60, #229954);
}

.region-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.region-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
}

.region-name {
  font-size: 1.3rem;
  font-weight: 600;
}

.region-stats-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 15px;
}

.region-stat {
  text-align: center;
}

.region-stat .stat-value {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.region-stat .stat-label {
  font-size: 0.85rem;
  opacity: 0.8;
}

.region-percentage {
  text-align: center;
  font-size: 0.9rem;
  opacity: 0.8;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 15px;
}

/* Estados */
.states-stats {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.states-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.state-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #007bff;
  transition: transform 0.3s ease;
}

.state-card:hover {
  transform: translateX(5px);
}

.state-rank {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.state-content {
  flex: 1;
}

.state-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.state-stats {
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
  color: #666;
}

.state-percentage {
  font-weight: 600;
  color: #007bff;
}

/* Atividade */
.activity-stats {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.activity-card {
  padding: 25px;
  background: #f8f9fa;
  border-radius: 12px;
  border-top: 4px solid #007bff;
}

.activity-card h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.2rem;
}

.activity-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item .label {
  color: #666;
  font-weight: 500;
}

.activity-item .value {
  color: #2c3e50;
  font-weight: 600;
}

.activity-item .value.growth {
  color: #28a745;
}

/* Sistema */
.system-info {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.system-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
}

.system-card {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #6c757d;
}

.system-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.system-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.system-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.system-item .label {
  color: #666;
}

.system-item .value {
  color: #2c3e50;
  font-weight: 500;
}

/* Atualização */
.update-info {
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.update-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.update-content {
  display: flex;
  gap: 10px;
  align-items: center;
}

.update-label {
  color: #666;
  font-weight: 500;
}

.update-time {
  color: #2c3e50;
  font-weight: 600;
}

/* Botões */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-outline:hover:not(:disabled) {
  background: white;
  color: #667eea;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsividade */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .regions-grid {
    grid-template-columns: 1fr;
  }
  
  .states-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-grid {
    grid-template-columns: 1fr;
  }
  
  .system-grid {
    grid-template-columns: 1fr;
  }
  
  .update-card {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .region-stats-content {
    grid-template-columns: 1fr;
  }
  
  .state-card {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
}
</style>

