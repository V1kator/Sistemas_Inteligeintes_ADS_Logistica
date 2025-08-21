<template>
  <div class="produtos-view">
    <div class="container">
      <!-- Header da Página -->
      <header class="page-header">
        <div class="header-content">
          <h1>Gestão de Produtos</h1>
          <p class="subtitle">Gerencie produtos e seus códigos de barras</p>
        </div>
        <div class="header-actions">
          <button @click="showCreateModal = true" class="btn btn-primary">
            <i class="icon">➕</i>
            Novo Produto
          </button>
        </div>
      </header>

      <!-- Filtros e Busca -->
      <section class="filters-section">
        <div class="filters-grid">
          <div class="filter-group">
            <label>Buscar produtos:</label>
            <input 
              v-model="searchTerm" 
              @input="debouncedSearch"
              type="text" 
              placeholder="Nome, CEP, cidade..."
              class="search-input"
            >
          </div>
          
          <div class="filter-group">
            <label>Estado:</label>
            <select v-model="filters.estado" @change="loadProducts">
              <option value="">Todos os estados</option>
              <option v-for="uf in estados" :key="uf" :value="uf">{{ uf }}</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Região:</label>
            <select v-model="filters.regiao" @change="loadProducts">
              <option value="">Todas as regiões</option>
              <option value="1">Norte/Nordeste</option>
              <option value="2">Centro-Oeste</option>
              <option value="3">Sul/Sudeste</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Por página:</label>
            <select v-model="pagination.per_page" @change="loadProducts">
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Lista de Produtos -->
      <section class="products-section">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Carregando produtos...</p>
        </div>

        <div v-else-if="products.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <h3>Nenhum produto encontrado</h3>
          <p>{{ searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece criando seu primeiro produto' }}</p>
          <button @click="showCreateModal = true" class="btn btn-primary">
            Criar Primeiro Produto
          </button>
        </div>

        <div v-else class="products-grid">
          <div 
            v-for="product in products" 
            :key="product.id"
            class="product-card"
            @click="viewProduct(product.id)"
          >
            <div class="product-header">
              <h3>{{ product.nome }}</h3>
              <div class="product-actions" @click.stop>
                <button @click="editProduct(product)" class="btn-icon" title="Editar">
                  ✏️
                </button>
                <button @click="deleteProduct(product)" class="btn-icon" title="Excluir">
                  🗑️
                </button>
              </div>
            </div>
            
            <div class="product-info">
              <div class="info-item">
                <span class="label">CEP:</span>
                <span class="value">{{ $formatCep(product.cep) }}</span>
              </div>
              <div class="info-item">
                <span class="label">Estado:</span>
                <span class="value">{{ product.estado }}</span>
              </div>
              <div class="info-item">
                <span class="label">Cidade:</span>
                <span class="value">{{ product.cidade }}</span>
              </div>
              <div class="info-item">
                <span class="label">Região:</span>
                <span class="value region" :class="`region-${product.regiao_identificador}`">
                  {{ $getRegionName(product.regiao_identificador) }}
                </span>
              </div>
            </div>
            
            <div class="product-stats">
              <div class="stat">
                <span class="stat-number">{{ product.total_codigos || 0 }}</span>
                <span class="stat-label">Códigos</span>
              </div>
              <div class="stat">
                <span class="stat-number">{{ product.total_downloads || 0 }}</span>
                <span class="stat-label">Downloads</span>
              </div>
            </div>
            
            <div class="product-footer">
              <span class="created-date">
                Criado em {{ $formatDate(product.data_criacao) }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Paginação -->
      <section v-if="pagination.pages > 1" class="pagination-section">
        <div class="pagination">
          <button 
            @click="changePage(pagination.page - 1)"
            :disabled="!pagination.has_prev"
            class="page-link"
          >
            ← Anterior
          </button>
          
          <span class="page-info">
            Página {{ pagination.page }} de {{ pagination.pages }}
            ({{ pagination.total }} produtos)
          </span>
          
          <button 
            @click="changePage(pagination.page + 1)"
            :disabled="!pagination.has_next"
            class="page-link"
          >
            Próxima →
          </button>
        </div>
      </section>
    </div>

    <!-- Modal de Criar/Editar Produto -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ showEditModal ? 'Editar Produto' : 'Novo Produto' }}</h3>
          <button @click="closeModals" class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="saveProduct">
            <div class="form-group">
              <label for="nome">Nome do Produto *</label>
              <input 
                id="nome"
                v-model="productForm.nome" 
                type="text" 
                required
                placeholder="Digite o nome do produto"
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
              >
              <div v-if="cepValidation.error" class="field-error">
                {{ cepValidation.error }}
              </div>
              <div v-if="cepValidation.loading" class="field-info">
                Consultando CEP...
              </div>
            </div>
            
            <div class="form-group">
              <label for="estado">Estado *</label>
              <select id="estado" v-model="productForm.estado" required>
                <option value="">Selecione o estado</option>
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
              >
            </div>
            
            <div class="form-group">
              <label for="descricao">Descrição</label>
              <textarea 
                id="descricao"
                v-model="productForm.descricao" 
                rows="3"
                placeholder="Descrição opcional do produto"
              ></textarea>
            </div>
            
            <div v-if="formErrors.length > 0" class="form-errors">
              <ul>
                <li v-for="error in formErrors" :key="error">{{ error }}</li>
              </ul>
            </div>
          </form>
        </div>
        
        <div class="modal-footer">
          <button @click="closeModals" type="button" class="btn btn-secondary">
            Cancelar
          </button>
          <button @click="saveProduct" type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Salvando...' : (showEditModal ? 'Atualizar' : 'Criar') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Confirmar Exclusão</h3>
          <button @click="closeModals" class="modal-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Tem certeza que deseja excluir o produto <strong>{{ productToDelete?.nome }}</strong>?</p>
          <p class="warning">Esta ação não pode ser desfeita e todos os códigos de barras associados também serão removidos.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="closeModals" class="btn btn-secondary">
            Cancelar
          </button>
          <button @click="confirmDelete" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? 'Excluindo...' : 'Excluir' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { productService, cepService } from '../services'

export default {
  name: 'ProdutosView',
  setup() {
    const router = useRouter()
    
    // Estados reativos
    const loading = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const products = ref([])
    const searchTerm = ref('')
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const showDeleteModal = ref(false)
    const productToDelete = ref(null)
    const formErrors = ref([])
    
    // Filtros e paginação
    const filters = reactive({
      estado: '',
      regiao: ''
    })
    
    const pagination = reactive({
      page: 1,
      per_page: 25,
      total: 0,
      pages: 0,
      has_next: false,
      has_prev: false
    })
    
    // Formulário de produto
    const productForm = reactive({
      id: null,
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
    
    // Debounce para busca
    let searchTimeout = null
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        pagination.page = 1
        loadProducts()
      }, 500)
    }
    
    // Métodos
    const loadProducts = async () => {
      try {
        loading.value = true
        
        const params = {
          page: pagination.page,
          per_page: pagination.per_page
        }
        
        if (searchTerm.value) params.search = searchTerm.value
        if (filters.estado) params.estado = filters.estado
        if (filters.regiao) params.regiao = filters.regiao
        
        const response = await productService.listProducts(params)
        
        if (response) {
          products.value = response.produtos || []
          Object.assign(pagination, response.paginacao || {})
        }
      } catch (error) {
        console.error('Erro ao carregar produtos:', error)
        if (window.showNotification) {
          window.showNotification('Erro ao carregar produtos', 'error')
        }
      } finally {
        loading.value = false
      }
    }
    
    const changePage = (page) => {
      pagination.page = page
      loadProducts()
    }
    
    const viewProduct = (id) => {
      router.push(`/produtos/${id}`)
    }
    
    const editProduct = (product) => {
      Object.assign(productForm, {
        id: product.id,
        nome: product.nome,
        cep: product.cep,
        estado: product.estado,
        cidade: product.cidade,
        descricao: product.descricao || ''
      })
      showEditModal.value = true
    }
    
    const deleteProduct = (product) => {
      productToDelete.value = product
      showDeleteModal.value = true
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
    
    const saveProduct = async () => {
      try {
        saving.value = true
        formErrors.value = []
        
        // Validação local
        const validation = productService.validateProduct(productForm)
        if (!validation.valid) {
          formErrors.value = validation.errors
          return
        }
        
        const productData = {
          nome: productForm.nome.trim(),
          cep: cepService.cleanCep(productForm.cep),
          estado: productForm.estado,
          cidade: productForm.cidade.trim(),
          descricao: productForm.descricao.trim()
        }
        
        let result
        if (showEditModal.value) {
          result = await productService.updateProduct(productForm.id, productData)
        } else {
          result = await productService.createProduct(productData)
        }
        
        if (result) {
          if (window.showNotification) {
            window.showNotification(
              `Produto ${showEditModal.value ? 'atualizado' : 'criado'} com sucesso`,
              'success'
            )
          }
          closeModals()
          loadProducts()
        }
      } catch (error) {
        console.error('Erro ao salvar produto:', error)
        formErrors.value = [error.message || 'Erro ao salvar produto']
      } finally {
        saving.value = false
      }
    }
    
    const confirmDelete = async () => {
      try {
        deleting.value = true
        
        const success = await productService.deleteProduct(productToDelete.value.id)
        
        if (success) {
          if (window.showNotification) {
            window.showNotification('Produto excluído com sucesso', 'success')
          }
          closeModals()
          loadProducts()
        }
      } catch (error) {
        console.error('Erro ao excluir produto:', error)
        if (window.showNotification) {
          window.showNotification('Erro ao excluir produto', 'error')
        }
      } finally {
        deleting.value = false
      }
    }
    
    const closeModals = () => {
      showCreateModal.value = false
      showEditModal.value = false
      showDeleteModal.value = false
      productToDelete.value = null
      
      // Reset form
      Object.assign(productForm, {
        id: null,
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
    
    // Lifecycle
    onMounted(() => {
      loadProducts()
    })
    
    return {
      loading,
      saving,
      deleting,
      products,
      searchTerm,
      filters,
      pagination,
      productForm,
      cepValidation,
      formErrors,
      estados,
      showCreateModal,
      showEditModal,
      showDeleteModal,
      productToDelete,
      debouncedSearch,
      loadProducts,
      changePage,
      viewProduct,
      editProduct,
      deleteProduct,
      applyCepMask,
      validateCep,
      saveProduct,
      confirmDelete,
      closeModals
    }
  }
}
</script>

<style scoped>
.produtos-view {
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
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 5px;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

/* Filtros */
.filters-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.filters-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 20px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 14px;
}

.search-input {
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #007bff;
  outline: none;
}

/* Produtos */
.products-section {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  min-height: 400px;
}

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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.product-card {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-card:hover {
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.15);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
}

.product-header h3 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.3rem;
  flex: 1;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  padding: 5px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.btn-icon:hover {
  background: rgba(0, 0, 0, 0.1);
}

.product-info {
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  color: #2c3e50;
}

.value.region {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.region-1 { background: #e74c3c; }
.region-2 { background: #f39c12; }
.region-3 { background: #27ae60; }

.product-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  padding: 10px 0;
  border-top: 1px solid #dee2e6;
}

.stat {
  text-align: center;
  flex: 1;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #007bff;
}

.stat-label {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
}

.product-footer {
  border-top: 1px solid #dee2e6;
  padding-top: 10px;
}

.created-date {
  font-size: 12px;
  color: #999;
}

/* Paginação */
.pagination-section {
  display: flex;
  justify-content: center;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px 30px;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.page-link {
  padding: 10px 20px;
  border: 2px solid #007bff;
  background: white;
  color: #007bff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.page-link:hover:not(:disabled) {
  background: #007bff;
  color: white;
}

.page-link:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-weight: 600;
  color: #2c3e50;
}

/* Formulários */
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

.warning {
  color: #856404;
  background: #fff3cd;
  padding: 10px;
  border-radius: 5px;
  border-left: 4px solid #ffc107;
}

/* Responsividade */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .pagination {
    flex-direction: column;
    gap: 15px;
  }
  
  .product-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .product-actions {
    align-self: flex-end;
  }
}
</style>

