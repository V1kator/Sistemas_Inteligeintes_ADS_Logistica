<template>
  <div class="gerar-codigo-view">
    <div class="container">
      <!-- Header da Página -->
      <header class="page-header">
        <div class="header-content">
          <h1>Gerar Código de Barras</h1>
          <p class="subtitle">Crie códigos de barras com identificadores regionais baseados em CEP</p>
        </div>
        <div class="header-visual">
          <div class="barcode-preview" v-if="generatedCode">
            <img :src="generatedCode.image_url" :alt="`Código ${generatedCode.codigo_completo}`">
            <div class="code-text">{{ generatedCode.codigo_completo }}</div>
          </div>
        </div>
      </header>

      <!-- Formulário de Geração -->
      <section class="generation-section">
        <div class="generation-grid">
          <!-- Formulário Principal -->
          <div class="form-card">
            <h3>Informações do Produto</h3>
            
            <form @submit.prevent="generateCode">
              <div class="form-group">
                <label for="produto-existente">Produto Existente:</label>
                <div class="product-selector">
                  <select 
                    id="produto-existente"
                    v-model="selectedProductId" 
                    @change="onProductSelect"
                  >
                    <option value="">Selecione um produto existente (opcional)</option>
                    <option v-for="product in products" :key="product.id" :value="product.id">
                      {{ product.nome }} - {{ $formatCep(product.cep) }}
                    </option>
                  </select>
                  <button 
                    type="button" 
                    @click="loadProducts" 
                    class="btn-refresh"
                    :disabled="loadingProducts"
                  >
                    🔄
                  </button>
                </div>
              </div>

              <div class="divider">
                <span>OU</span>
              </div>

              <div class="form-group">
                <label for="nome">Nome do Produto *</label>
                <input 
                  id="nome"
                  v-model="productForm.nome" 
                  type="text" 
                  required
                  placeholder="Digite o nome do produto"
                  :disabled="selectedProductId"
                >
              </div>
              
              <div class="form-group">
                <label for="cep">CEP *</label>
                <input 
                  id="cep"
                  v-model="productForm.cep" 
                  type="text" 
                  required
                  placeholder="00000-000"
                  @input="applyCepMask"
                  @blur="validateCep"
                  maxlength="9"
                  :disabled="selectedProductId"
                >
                <div v-if="cepValidation.error" class="field-error">
                  {{ cepValidation.error }}
                </div>
                <div v-if="cepValidation.loading" class="field-info">
                  Consultando CEP...
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="estado">Estado *</label>
                  <select 
                    id="estado" 
                    v-model="productForm.estado" 
                    required
                    :disabled="selectedProductId"
                  >
                    <option value="">Selecione</option>
                    <option v-for="uf in estados" :key="uf" :value="uf">{{ uf }}</option>
                  </select>
                </div>
                
                <div class="form-group">
                  <label for="cidade">Cidade *</label>
                  <input 
                    id="cidade"
                    v-model="productForm.cidade" 
                    type="text" 
                    required
                    placeholder="Digite a cidade"
                    :disabled="selectedProductId"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="descricao">Descrição</label>
                <textarea 
                  id="descricao"
                  v-model="productForm.descricao" 
                  rows="3"
                  placeholder="Descrição opcional do produto"
                  :disabled="selectedProductId"
                ></textarea>
              </div>
              
              <div v-if="formErrors.length > 0" class="form-errors">
                <ul>
                  <li v-for="error in formErrors" :key="error">{{ error }}</li>
                </ul>
              </div>

              <button 
                type="submit" 
                class="btn btn-primary btn-large"
                :disabled="generating || !canGenerate"
              >
                <i class="icon">🏷️</i>
                {{ generating ? 'Gerando...' : 'Gerar Código de Barras' }}
              </button>
            </form>
          </div>

          <!-- Informações da Região -->
          <div class="info-card">
            <h3>Identificador Regional</h3>
            
            <div v-if="regionInfo" class="region-display">
              <div class="region-badge" :class="`region-${regionInfo.id}`">
                <div class="region-number">{{ regionInfo.id }}</div>
                <div class="region-name">{{ regionInfo.nome }}</div>
              </div>
              
              <div class="region-details">
                <p><strong>Estados incluídos:</strong></p>
                <div class="states-grid">
                  <span 
                    v-for="estado in regionInfo.estados" 
                    :key="estado"
                    class="state-badge"
                    :class="{ active: estado === productForm.estado }"
                  >
                    {{ estado }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-else class="region-placeholder">
              <p>Preencha o estado para ver o identificador regional</p>
            </div>

            <!-- Explicação do Sistema -->
            <div class="explanation">
              <h4>Como funciona?</h4>
              <ul>
                <li><strong>Identificador 1:</strong> Norte e Nordeste</li>
                <li><strong>Identificador 2:</strong> Centro-Oeste</li>
                <li><strong>Identificador 3:</strong> Sul e Sudeste</li>
              </ul>
              <p>O código gerado terá o formato: <code>[ID][12 caracteres únicos]</code></p>
            </div>
          </div>
        </div>
      </section>

      <!-- Resultado da Geração -->
      <section v-if="generatedCode" class="result-section">
        <div class="result-card">
          <h3>Código Gerado com Sucesso!</h3>
          
          <div class="result-content">
            <div class="barcode-display">
              <img 
                :src="generatedCode.image_url" 
                :alt="`Código ${generatedCode.codigo_completo}`"
                class="barcode-image"
              >
              <div class="code-info">
                <div class="code-number">{{ generatedCode.codigo_completo }}</div>
                <div class="code-details">
                  <span class="region-indicator">
                    Região {{ generatedCode.regiao_identificador }}: 
                    {{ $getRegionName(generatedCode.regiao_identificador) }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="result-actions">
              <button @click="downloadCode" class="btn btn-success">
                <i class="icon">💾</i>
                Download PNG
              </button>
              
              <button @click="generateAnother" class="btn btn-secondary">
                <i class="icon">🔄</i>
                Gerar Outro
              </button>
              
              <button @click="viewProduct" class="btn btn-outline" v-if="generatedCode.produto_id">
                <i class="icon">👁️</i>
                Ver Produto
              </button>
            </div>
          </div>
          
          <div class="result-metadata">
            <div class="metadata-item">
              <span class="label">Produto:</span>
              <span class="value">{{ generatedCode.produto_nome }}</span>
            </div>
            <div class="metadata-item">
              <span class="label">CEP:</span>
              <span class="value">{{ $formatCep(generatedCode.produto_cep) }}</span>
            </div>
            <div class="metadata-item">
              <span class="label">Localização:</span>
              <span class="value">{{ generatedCode.produto_cidade }}, {{ generatedCode.produto_estado }}</span>
            </div>
            <div class="metadata-item">
              <span class="label">Gerado em:</span>
              <span class="value">{{ $formatDateTime(generatedCode.data_criacao) }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Histórico de Códigos Gerados -->
      <section class="history-section">
        <div class="history-header">
          <h3>Códigos Recentes</h3>
          <button @click="loadRecentCodes" class="btn btn-outline btn-sm">
            <i class="icon">🔄</i>
            Atualizar
          </button>
        </div>
        
        <div v-if="loadingHistory" class="loading">
          <div class="spinner"></div>
          <p>Carregando histórico...</p>
        </div>
        
        <div v-else-if="recentCodes.length === 0" class="empty-history">
          <p>Nenhum código gerado recentemente</p>
        </div>
        
        <div v-else class="codes-grid">
          <div 
            v-for="code in recentCodes" 
            :key="code.id"
            class="code-card"
          >
            <div class="code-preview">
              <img :src="code.image_url" :alt="`Código ${code.codigo_completo}`">
            </div>
            
            <div class="code-info">
              <div class="code-number">{{ code.codigo_completo }}</div>
              <div class="code-product">{{ code.produto_nome }}</div>
              <div class="code-location">
                {{ code.produto_cidade }}, {{ code.produto_estado }}
              </div>
              <div class="code-date">
                {{ $formatDate(code.data_criacao) }}
              </div>
            </div>
            
            <div class="code-actions">
              <button @click="downloadCodeById(code.id)" class="btn-icon" title="Download">
                💾
              </button>
              <button @click="viewProductById(code.produto_id)" class="btn-icon" title="Ver Produto">
                👁️
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { productService, cepService, barcodeService } from '../services'

export default {
  name: 'GerarCodigoView',
  setup() {
    const router = useRouter()
    
    // Estados reativos
    const generating = ref(false)
    const loadingProducts = ref(false)
    const loadingHistory = ref(false)
    const products = ref([])
    const recentCodes = ref([])
    const selectedProductId = ref('')
    const generatedCode = ref(null)
    const formErrors = ref([])
    
    // Formulário de produto
    const productForm = reactive({
      nome: '',
      cep: '',
      estado: '',
      cidade: '',
      descricao: ''
    })
    
    // Validação de CEP
    const cepValidation = reactive({
      loading: false,
      error: '',
      valid: false
    })
    
    // Estados brasileiros
    const estados = [
      'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
      'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
      'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    // Mapeamento de regiões
    const regionMapping = {
      'AC': { id: 1, nome: 'Norte/Nordeste' },
      'AL': { id: 1, nome: 'Norte/Nordeste' },
      'AP': { id: 1, nome: 'Norte/Nordeste' },
      'AM': { id: 1, nome: 'Norte/Nordeste' },
      'BA': { id: 1, nome: 'Norte/Nordeste' },
      'CE': { id: 1, nome: 'Norte/Nordeste' },
      'MA': { id: 1, nome: 'Norte/Nordeste' },
      'PA': { id: 1, nome: 'Norte/Nordeste' },
      'PB': { id: 1, nome: 'Norte/Nordeste' },
      'PE': { id: 1, nome: 'Norte/Nordeste' },
      'PI': { id: 1, nome: 'Norte/Nordeste' },
      'RN': { id: 1, nome: 'Norte/Nordeste' },
      'RO': { id: 1, nome: 'Norte/Nordeste' },
      'RR': { id: 1, nome: 'Norte/Nordeste' },
      'SE': { id: 1, nome: 'Norte/Nordeste' },
      'TO': { id: 1, nome: 'Norte/Nordeste' },
      'DF': { id: 2, nome: 'Centro-Oeste' },
      'GO': { id: 2, nome: 'Centro-Oeste' },
      'MT': { id: 2, nome: 'Centro-Oeste' },
      'MS': { id: 2, nome: 'Centro-Oeste' },
      'ES': { id: 3, nome: 'Sul/Sudeste' },
      'MG': { id: 3, nome: 'Sul/Sudeste' },
      'RJ': { id: 3, nome: 'Sul/Sudeste' },
      'SP': { id: 3, nome: 'Sul/Sudeste' },
      'PR': { id: 3, nome: 'Sul/Sudeste' },
      'RS': { id: 3, nome: 'Sul/Sudeste' },
      'SC': { id: 3, nome: 'Sul/Sudeste' }
    }
    
    // Computed properties
    const canGenerate = computed(() => {
      return productForm.nome && productForm.cep && productForm.estado && productForm.cidade
    })
    
    const regionInfo = computed(() => {
      if (!productForm.estado) return null
      
      const region = regionMapping[productForm.estado]
      if (!region) return null
      
      const estadosPorRegiao = {
        1: ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'MA', 'PA', 'PB', 'PE', 'PI', 'RN', 'RO', 'RR', 'SE', 'TO'],
        2: ['DF', 'GO', 'MT', 'MS'],
        3: ['ES', 'MG', 'RJ', 'SP', 'PR', 'RS', 'SC']
      }
      
      return {
        ...region,
        estados: estadosPorRegiao[region.id] || []
      }
    })
    
    // Métodos
    const loadProducts = async () => {
      try {
        loadingProducts.value = true
        const response = await productService.listProducts({ per_page: 100 })
        
        if (response && response.produtos) {
          products.value = response.produtos
        }
      } catch (error) {
        console.error('Erro ao carregar produtos:', error)
      } finally {
        loadingProducts.value = false
      }
    }
    
    const onProductSelect = () => {
      if (selectedProductId.value) {
        const product = products.value.find(p => p.id == selectedProductId.value)
        if (product) {
          Object.assign(productForm, {
            nome: product.nome,
            cep: product.cep,
            estado: product.estado,
            cidade: product.cidade,
            descricao: product.descricao || ''
          })
        }
      } else {
        // Limpa o formulário
        Object.assign(productForm, {
          nome: '',
          cep: '',
          estado: '',
          cidade: '',
          descricao: ''
        })
      }
    }
    
    const applyCepMask = (event) => {
      const value = event.target.value
      productForm.cep = cepService.applyCepMask(value)
    }
    
    const validateCep = async () => {
      const cep = cepService.cleanCep(productForm.cep)
      
      if (!cep) {
        cepValidation.error = ''
        cepValidation.valid = false
        return
      }
      
      if (!cepService.validateCep(cep)) {
        cepValidation.error = 'CEP inválido'
        cepValidation.valid = false
        return
      }
      
      try {
        cepValidation.loading = true
        cepValidation.error = ''
        
        const cepData = await cepService.consultarCep(cep)
        
        if (cepData) {
          productForm.estado = cepData.uf
          productForm.cidade = cepData.localidade
          cepValidation.valid = true
          
          if (window.showNotification) {
            window.showNotification('CEP encontrado e dados preenchidos', 'success')
          }
        } else {
          cepValidation.error = 'CEP não encontrado'
          cepValidation.valid = false
        }
      } catch (error) {
        cepValidation.error = 'Erro ao consultar CEP'
        cepValidation.valid = false
      } finally {
        cepValidation.loading = false
      }
    }
    
    const generateCode = async () => {
      try {
        generating.value = true
        formErrors.value = []
        
        // Validação local
        const validation = productService.validateProduct(productForm)
        if (!validation.valid) {
          formErrors.value = validation.errors
          return
        }
        
        let productId = selectedProductId.value
        
        // Se não há produto selecionado, cria um novo
        if (!productId) {
          const productData = {
            nome: productForm.nome.trim(),
            cep: cepService.cleanCep(productForm.cep),
            estado: productForm.estado,
            cidade: productForm.cidade.trim(),
            descricao: productForm.descricao.trim()
          }
          
          const newProduct = await productService.createProduct(productData)
          if (!newProduct) {
            throw new Error('Erro ao criar produto')
          }
          productId = newProduct.id
        }
        
        // Gera o código de barras
        const codeData = {
          produto_id: productId
        }
        
        const result = await barcodeService.generateBarcode(codeData)
        
        if (result) {
          generatedCode.value = result
          
          if (window.showNotification) {
            window.showNotification('Código de barras gerado com sucesso!', 'success')
          }
          
          // Atualiza o histórico
          loadRecentCodes()
        }
      } catch (error) {
        console.error('Erro ao gerar código:', error)
        formErrors.value = [error.message || 'Erro ao gerar código de barras']
        
        if (window.showNotification) {
          window.showNotification('Erro ao gerar código de barras', 'error')
        }
      } finally {
        generating.value = false
      }
    }
    
    const downloadCode = async () => {
      if (!generatedCode.value) return
      
      try {
        await barcodeService.downloadBarcode(generatedCode.value.id)
        
        if (window.showNotification) {
          window.showNotification('Download iniciado!', 'success')
        }
      } catch (error) {
        console.error('Erro ao fazer download:', error)
        if (window.showNotification) {
          window.showNotification('Erro ao fazer download', 'error')
        }
      }
    }
    
    const downloadCodeById = async (codeId) => {
      try {
        await barcodeService.downloadBarcode(codeId)
        
        if (window.showNotification) {
          window.showNotification('Download iniciado!', 'success')
        }
      } catch (error) {
        console.error('Erro ao fazer download:', error)
        if (window.showNotification) {
          window.showNotification('Erro ao fazer download', 'error')
        }
      }
    }
    
    const generateAnother = () => {
      generatedCode.value = null
      selectedProductId.value = ''
      Object.assign(productForm, {
        nome: '',
        cep: '',
        estado: '',
        cidade: '',
        descricao: ''
      })
      formErrors.value = []
      cepValidation.error = ''
      cepValidation.valid = false
    }
    
    const viewProduct = () => {
      if (generatedCode.value && generatedCode.value.produto_id) {
        router.push(`/produtos/${generatedCode.value.produto_id}`)
      }
    }
    
    const viewProductById = (productId) => {
      router.push(`/produtos/${productId}`)
    }
    
    const loadRecentCodes = async () => {
      try {
        loadingHistory.value = true
        const response = await barcodeService.listBarcodes({ per_page: 6 })
        
        if (response && response.codigos) {
          recentCodes.value = response.codigos
        }
      } catch (error) {
        console.error('Erro ao carregar códigos recentes:', error)
      } finally {
        loadingHistory.value = false
      }
    }
    
    // Lifecycle
    onMounted(() => {
      loadProducts()
      loadRecentCodes()
    })
    
    return {
      generating,
      loadingProducts,
      loadingHistory,
      products,
      recentCodes,
      selectedProductId,
      generatedCode,
      productForm,
      cepValidation,
      formErrors,
      estados,
      canGenerate,
      regionInfo,
      loadProducts,
      onProductSelect,
      applyCepMask,
      validateCep,
      generateCode,
      downloadCode,
      downloadCodeById,
      generateAnother,
      viewProduct,
      viewProductById,
      loadRecentCodes
    }
  }
}
</script>

<style scoped>
.gerar-codigo-view {
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
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 40px;
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
  margin-bottom: 10px;
  color: white;
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

.header-visual {
  display: flex;
  justify-content: center;
}

.barcode-preview {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.barcode-preview img {
  max-width: 200px;
  height: auto;
  margin-bottom: 10px;
}

.code-text {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: #333;
}

/* Seção de Geração */
.generation-section {
  margin-bottom: 40px;
}

.generation-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.form-card,
.info-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.form-card h3,
.info-card h3 {
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 1.5rem;
}

/* Formulário */
.product-selector {
  display: flex;
  gap: 10px;
  align-items: center;
}

.product-selector select {
  flex: 1;
}

.btn-refresh {
  padding: 12px;
  border: 2px solid #007bff;
  background: white;
  color: #007bff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-refresh:hover:not(:disabled) {
  background: #007bff;
  color: white;
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.divider {
  text-align: center;
  margin: 25px 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #dee2e6;
}

.divider span {
  background: white;
  padding: 0 15px;
  color: #666;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #007bff;
  outline: none;
}

.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  background: #f8f9fa;
  color: #6c757d;
}

.field-error {
  color: #dc3545;
  font-size: 14px;
  margin-top: 5px;
}

.field-info {
  color: #007bff;
  font-size: 14px;
  margin-top: 5px;
}

.form-errors {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.form-errors ul {
  margin: 0;
  padding-left: 20px;
  color: #721c24;
}

.btn-large {
  padding: 16px 32px;
  font-size: 18px;
  width: 100%;
  justify-content: center;
}

/* Informações da Região */
.region-display {
  margin-bottom: 25px;
}

.region-badge {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.region-badge.region-1 {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.region-badge.region-2 {
  background: linear-gradient(135deg, #f39c12, #e67e22);
  color: white;
}

.region-badge.region-3 {
  background: linear-gradient(135deg, #27ae60, #229954);
  color: white;
}

.region-number {
  font-size: 2rem;
  font-weight: 800;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.region-name {
  font-size: 1.2rem;
  font-weight: 600;
}

.states-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 8px;
  margin-top: 10px;
}

.state-badge {
  padding: 5px 8px;
  background: #e9ecef;
  border-radius: 15px;
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: #495057;
  transition: all 0.3s ease;
}

.state-badge.active {
  background: #007bff;
  color: white;
  transform: scale(1.1);
}

.region-placeholder {
  text-align: center;
  padding: 40px 20px;
  color: #666;
  background: #f8f9fa;
  border-radius: 10px;
}

.explanation {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

.explanation h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.explanation ul {
  margin-bottom: 15px;
}

.explanation code {
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

/* Resultado */
.result-section {
  margin-bottom: 40px;
}

.result-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid #28a745;
}

.result-card h3 {
  color: #28a745;
  margin-bottom: 25px;
  text-align: center;
}

.result-content {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 30px;
  align-items: center;
  margin-bottom: 25px;
}

.barcode-display {
  text-align: center;
}

.barcode-image {
  max-width: 300px;
  height: auto;
  margin-bottom: 15px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 10px;
  background: white;
}

.code-number {
  font-family: 'Courier New', monospace;
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 10px;
}

.region-indicator {
  background: #e9ecef;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 14px;
  color: #495057;
}

.result-actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.result-metadata {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.metadata-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.metadata-item .label {
  font-weight: 600;
  color: #666;
  font-size: 14px;
}

.metadata-item .value {
  color: #2c3e50;
}

/* Histórico */
.history-section {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.history-header h3 {
  color: #2c3e50;
  margin: 0;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #666;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-history {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.codes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.code-card {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 15px;
  transition: all 0.3s ease;
}

.code-card:hover {
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.15);
}

.code-preview {
  text-align: center;
  margin-bottom: 15px;
}

.code-preview img {
  max-width: 100%;
  height: 60px;
  object-fit: contain;
}

.code-info {
  margin-bottom: 15px;
}

.code-info .code-number {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 5px;
}

.code-product {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 3px;
}

.code-location,
.code-date {
  font-size: 12px;
  color: #666;
}

.code-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn-icon {
  background: none;
  border: 1px solid #dee2e6;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background: #f8f9fa;
  border-color: #007bff;
}

/* Responsividade */
@media (max-width: 768px) {
  .page-header {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .generation-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .result-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .result-metadata {
    grid-template-columns: 1fr;
  }
  
  .codes-grid {
    grid-template-columns: 1fr;
  }
  
  .states-grid {
    grid-template-columns: repeat(auto-fill, minmax(35px, 1fr));
  }
}
</style>

