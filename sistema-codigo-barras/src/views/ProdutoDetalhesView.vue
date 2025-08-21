<template>
  <div class="produto-detalhes-view">
    <div class="container">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Carregando produto...</p>
      </div>

      <div v-else-if="!product" class="not-found">
        <h1>Produto não encontrado</h1>
        <p>O produto solicitado não foi encontrado.</p>
        <router-link to="/produtos" class="btn btn-primary">
          Voltar para Produtos
        </router-link>
      </div>

      <div v-else>
        <!-- Header do Produto -->
        <header class="product-header">
          <div class="header-content">
            <h1>{{ product.nome }}</h1>
            <p class="product-description">{{ product.descricao || 'Sem descrição' }}</p>
          </div>
          <div class="header-actions">
            <button @click="editProduct" class="btn btn-secondary">
              ✏️ Editar
            </button>
            <button @click="generateCode" class="btn btn-primary">
              🏷️ Gerar Código
            </button>
          </div>
        </header>

        <!-- Informações do Produto -->
        <section class="product-info">
          <div class="info-grid">
            <div class="info-card">
              <h3>📍 Localização</h3>
              <div class="info-content">
                <div class="info-item">
                  <span class="label">CEP:</span>
                  <span class="value">{{ $formatCep(product.cep) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Cidade:</span>
                  <span class="value">{{ product.cidade }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Estado:</span>
                  <span class="value">{{ product.estado }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Região:</span>
                  <span class="value region" :class="`region-${product.regiao_identificador}`">
                    {{ $getRegionName(product.regiao_identificador) }}
                  </span>
                </div>
              </div>
            </div>

            <div class="info-card">
              <h3>📊 Estatísticas</h3>
              <div class="stats-content">
                <div class="stat">
                  <div class="stat-number">{{ product.total_codigos || 0 }}</div>
                  <div class="stat-label">Códigos Gerados</div>
                </div>
                <div class="stat">
                  <div class="stat-number">{{ product.total_downloads || 0 }}</div>
                  <div class="stat-label">Downloads</div>
                </div>
              </div>
            </div>

            <div class="info-card">
              <h3>📅 Datas</h3>
              <div class="info-content">
                <div class="info-item">
                  <span class="label">Criado em:</span>
                  <span class="value">{{ $formatDateTime(product.data_criacao) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Atualizado em:</span>
                  <span class="value">{{ $formatDateTime(product.data_atualizacao) }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Códigos de Barras -->
        <section class="barcodes-section">
          <div class="section-header">
            <h2>Códigos de Barras</h2>
            <button @click="loadBarcodes" class="btn btn-outline btn-sm">
              🔄 Atualizar
            </button>
          </div>

          <div v-if="loadingBarcodes" class="loading">
            <div class="spinner"></div>
            <p>Carregando códigos...</p>
          </div>

          <div v-else-if="barcodes.length === 0" class="empty-barcodes">
            <div class="empty-icon">🏷️</div>
            <h3>Nenhum código gerado</h3>
            <p>Este produto ainda não possui códigos de barras.</p>
            <button @click="generateCode" class="btn btn-primary">
              Gerar Primeiro Código
            </button>
          </div>

          <div v-else class="barcodes-grid">
            <div 
              v-for="barcode in barcodes" 
              :key="barcode.id"
              class="barcode-card"
            >
              <div class="barcode-image">
                <img :src="barcode.image_url" :alt="`Código ${barcode.codigo_completo}`">
              </div>
              
              <div class="barcode-info">
                <div class="code-number">{{ barcode.codigo_completo }}</div>
                <div class="code-details">
                  <span class="region-badge" :class="`region-${barcode.regiao_identificador}`">
                    Região {{ barcode.regiao_identificador }}
                  </span>
                  <span class="downloads">{{ barcode.total_downloads || 0 }} downloads</span>
                </div>
                <div class="code-date">
                  Gerado em {{ $formatDate(barcode.data_criacao) }}
                </div>
              </div>
              
              <div class="barcode-actions">
                <button @click="downloadBarcode(barcode.id)" class="btn-icon" title="Download">
                  💾
                </button>
                <button @click="copyCode(barcode.codigo_completo)" class="btn-icon" title="Copiar">
                  📋
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productService, barcodeService } from '../services'

export default {
  name: 'ProdutoDetalhesView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const loading = ref(true)
    const loadingBarcodes = ref(false)
    const product = ref(null)
    const barcodes = ref([])
    
    const loadProduct = async () => {
      try {
        loading.value = true
        const productId = route.params.id
        
        const productData = await productService.getProduct(productId)
        
        if (productData) {
          product.value = productData
          await loadBarcodes()
        } else {
          product.value = null
        }
      } catch (error) {
        console.error('Erro ao carregar produto:', error)
        product.value = null
      } finally {
        loading.value = false
      }
    }
    
    const loadBarcodes = async () => {
      if (!product.value) return
      
      try {
        loadingBarcodes.value = true
        const barcodesData = await productService.getProductBarcodes(product.value.id)
        barcodes.value = barcodesData || []
      } catch (error) {
        console.error('Erro ao carregar códigos:', error)
        barcodes.value = []
      } finally {
        loadingBarcodes.value = false
      }
    }
    
    const editProduct = () => {
      router.push(`/produtos?edit=${product.value.id}`)
    }
    
    const generateCode = () => {
      router.push(`/gerar?produto=${product.value.id}`)
    }
    
    const downloadBarcode = async (barcodeId) => {
      try {
        await barcodeService.downloadBarcode(barcodeId)
        
        if (window.showNotification) {
          window.showNotification('Download iniciado!', 'success')
        }
        
        // Atualiza a contagem de downloads
        loadBarcodes()
      } catch (error) {
        console.error('Erro ao fazer download:', error)
        if (window.showNotification) {
          window.showNotification('Erro ao fazer download', 'error')
        }
      }
    }
    
    const copyCode = async (code) => {
      try {
        await navigator.clipboard.writeText(code)
        
        if (window.showNotification) {
          window.showNotification('Código copiado!', 'success')
        }
      } catch (error) {
        console.error('Erro ao copiar código:', error)
        if (window.showNotification) {
          window.showNotification('Erro ao copiar código', 'error')
        }
      }
    }
    
    onMounted(() => {
      loadProduct()
    })
    
    return {
      loading,
      loadingBarcodes,
      product,
      barcodes,
      loadBarcodes,
      editProduct,
      generateCode,
      downloadBarcode,
      copyCode
    }
  }
}
</script>

<style scoped>
.produto-detalhes-view {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Loading e Estados */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.not-found {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.not-found h1 {
  color: #dc3545;
  margin-bottom: 20px;
}

/* Header do Produto */
.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.header-content h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: white;
}

.product-description {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 15px;
}

/* Informações do Produto */
.product-info {
  margin-bottom: 40px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.info-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-card h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.3rem;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  color: #2c3e50;
  font-weight: 500;
}

.value.region {
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.region-1 { background: #e74c3c; }
.region-2 { background: #f39c12; }
.region-3 { background: #27ae60; }

/* Estatísticas */
.stats-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #007bff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  text-transform: uppercase;
  font-weight: 600;
}

/* Seção de Códigos */
.barcodes-section {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.section-header h2 {
  color: #2c3e50;
  margin: 0;
}

.empty-barcodes {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-barcodes h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

/* Grid de Códigos */
.barcodes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.barcode-card {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.barcode-card:hover {
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.15);
}

.barcode-image {
  text-align: center;
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
}

.barcode-image img {
  max-width: 100%;
  height: 80px;
  object-fit: contain;
}

.barcode-info {
  margin-bottom: 20px;
}

.code-number {
  font-family: 'Courier New', monospace;
  font-size: 1.1rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 10px;
  text-align: center;
}

.code-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.region-badge {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.downloads {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.code-date {
  font-size: 12px;
  color: #999;
  text-align: center;
}

.barcode-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

/* Botões */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.btn-icon {
  background: none;
  border: 1px solid #dee2e6;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
}

.btn-icon:hover {
  background: #f8f9fa;
  border-color: #007bff;
  transform: scale(1.1);
}

/* Responsividade */
@media (max-width: 768px) {
  .product-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .header-content h1 {
    font-size: 2rem;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-content {
    grid-template-columns: 1fr;
  }
  
  .barcodes-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .code-details {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 15px;
  }
  
  .product-header {
    padding: 25px;
  }
  
  .info-card {
    padding: 20px;
  }
  
  .barcodes-section {
    padding: 20px;
  }
  
  .barcode-card {
    padding: 15px;
  }
}
</style>

