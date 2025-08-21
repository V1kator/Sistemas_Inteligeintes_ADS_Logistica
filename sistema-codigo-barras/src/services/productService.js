/**
 * Serviço para comunicação com API de produtos
 */

const API_BASE_URL = import.meta.env.VUE_APP_API_URL || 'http://localhost:5000/api'

class ProductService {
  /**
   * Lista produtos com paginação e filtros
   * @param {Object} params - Parâmetros de busca
   * @returns {Promise<Object>} Lista paginada de produtos
   */
  async listProducts(params = {}) {
    try {
      const queryParams = new URLSearchParams()

      if (params.page) queryParams.append('page', params.page)
      if (params.per_page) queryParams.append('per_page', params.per_page)
      if (params.search) queryParams.append('search', params.search)
      if (params.estado) queryParams.append('estado', params.estado)
      if (params.regiao) queryParams.append('regiao', params.regiao)

      const url = `${API_BASE_URL}/produtos/?${queryParams.toString()}`
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao listar produtos:', error)
      throw error
    }
  }

  /**
   * Obtém um produto por ID
   * @param {number} id - ID do produto
   * @returns {Promise<Object>} Dados do produto
   */
  async getProduct(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos/${id}`)

      if (!response.ok) {
        if (response.status === 404) {
          return null
        }
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao obter produto:', error)
      throw error
    }
  }

  /**
   * Cria um novo produto
   * @param {Object} productData - Dados do produto
   * @returns {Promise<Object>} Produto criado
   */
  async createProduct(productData) {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || `Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao criar produto:', error)
      throw error
    }
  }

  /**
   * Atualiza um produto existente
   * @param {number} id - ID do produto
   * @param {Object} productData - Dados atualizados
   * @returns {Promise<Object>} Produto atualizado
   */
  async updateProduct(id, productData) {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || `Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao atualizar produto:', error)
      throw error
    }
  }

  /**
   * Deleta um produto
   * @param {number} id - ID do produto
   * @returns {Promise<boolean>} Sucesso da operação
   */
  async deleteProduct(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos/${id}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success
    } catch (error) {
      console.error('Erro ao deletar produto:', error)
      throw error
    }
  }

  /**
   * Busca produtos por termo
   * @param {string} term - Termo de busca
   * @param {Object} params - Parâmetros adicionais
   * @returns {Promise<Object>} Resultados da busca
   */
  async searchProducts(term, params = {}) {
    try {
      const queryParams = new URLSearchParams()
      queryParams.append('termo', term)

      if (params.page) queryParams.append('page', params.page)
      if (params.per_page) queryParams.append('per_page', params.per_page)

      const url = `${API_BASE_URL}/produtos/buscar?${queryParams.toString()}`
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao buscar produtos:', error)
      throw error
    }
  }

  /**
   * Obtém códigos de barras de um produto
   * @param {number} productId - ID do produto
   * @returns {Promise<Array>} Lista de códigos do produto
   */
  async getProductBarcodes(productId) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/produto/${productId}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : []
    } catch (error) {
      console.error('Erro ao obter códigos do produto:', error)
      throw error
    }
  }

  /**
   * Valida dados de produto antes do envio
   * @param {Object} productData - Dados do produto
   * @returns {Object} Resultado da validação
   */
  validateProduct(productData) {
    const errors = []

    if (!productData.nome || productData.nome.trim().length < 2) {
      errors.push('Nome deve ter pelo menos 2 caracteres')
    }

    if (!productData.cep || !/^\d{5}-?\d{3}$/.test(productData.cep)) {
      errors.push('CEP deve estar no formato 00000-000')
    }

    if (!productData.estado || productData.estado.length !== 2) {
      errors.push('Estado deve ter 2 caracteres (UF)')
    }

    if (!productData.cidade || productData.cidade.trim().length < 2) {
      errors.push('Cidade deve ter pelo menos 2 caracteres')
    }

    return {
      valid: errors.length === 0,
      errors
    }
  }

  /**
   * Formata CEP para exibição
   * @param {string} cep - CEP sem formatação
   * @returns {string} CEP formatado
   */
  formatCep(cep) {
    if (!cep) return ''
    const cleaned = cep.replace(/\D/g, '')
    if (cleaned.length === 8) {
      return `${cleaned.slice(0, 5)}-${cleaned.slice(5)}`
    }
    return cep
  }

  /**
   * Remove formatação do CEP
   * @param {string} cep - CEP formatado
   * @returns {string} CEP apenas números
   */
  cleanCep(cep) {
    return cep ? cep.replace(/\D/g, '') : ''
  }

  /**
   * Obtém estatísticas de produtos
   * @returns {Promise<Object>} Estatísticas
   */
  async getProductStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos/stats`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao obter estatísticas de produtos:', error)
      throw error
    }
  }

  /**
   * Exporta produtos para CSV
   * @param {Object} filters - Filtros para exportação
   * @returns {Promise<Blob>} Arquivo CSV
   */
  async exportProducts(filters = {}) {
    try {
      const queryParams = new URLSearchParams()

      if (filters.estado) queryParams.append('estado', filters.estado)
      if (filters.regiao) queryParams.append('regiao', filters.regiao)
      if (filters.data_inicio) queryParams.append('data_inicio', filters.data_inicio)
      if (filters.data_fim) queryParams.append('data_fim', filters.data_fim)

      const url = `${API_BASE_URL}/produtos/exportar?${queryParams.toString()}`
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      return await response.blob()
    } catch (error) {
      console.error('Erro ao exportar produtos:', error)
      throw error
    }
  }
}

// Instância singleton do serviço
export const productService = new ProductService()

// Exporta também a classe para casos específicos
export default ProductService

