/**
 * Serviço para comunicação com API de códigos de barras
 */

const API_BASE_URL = import.meta.env.VUE_APP_API_URL || 'http://localhost:5000/api'

class BarcodeService {
  /**
   * Busca código de barras pelo código completo
   * @param {string} code - Código completo do código de barras
   * @returns {Promise<Object>} Dados do código de barras e produto
   */
  async searchByCode(code) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/buscar/${code}`)

      if (!response.ok) {
        if (response.status === 404) {
          return null
        }
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao buscar código de barras:', error)
      throw error
    }
  }

  /**
   * Obtém informações de um código de barras por ID
   * @param {number} id - ID do código de barras
   * @returns {Promise<Object>} Dados do código de barras
   */
  async getById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/${id}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao obter código de barras:', error)
      throw error
    }
  }

  /**
   * Gera um novo código de barras para um produto
   * @param {number} produtoId - ID do produto
   * @param {number} regiaoId - ID da região (opcional)
   * @returns {Promise<Object>} Código de barras gerado
   */
  async generateBarcode(produtoId, regiaoId = null) {
    try {
      const body = { produto_id: produtoId }
      if (regiaoId) {
        body.regiao_id = regiaoId
      }

      const response = await fetch(`${API_BASE_URL}/codigos-barras/gerar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      })

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao gerar código de barras:', error)
      throw error
    }
  }

  /**
   * Faz download do arquivo PNG do código de barras
   * @param {number} id - ID do código de barras
   * @returns {Promise<void>}
   */
  async downloadBarcode(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/download/${id}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      // Obtém o blob da resposta
      const blob = await response.blob()

      // Cria URL temporária para download
      const url = window.URL.createObjectURL(blob)

      // Cria elemento de link temporário para download
      const link = document.createElement('a')
      link.href = url
      link.download = `codigo_barras_${id}.png`
      document.body.appendChild(link)
      link.click()

      // Limpa recursos
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)

    } catch (error) {
      console.error('Erro ao baixar código de barras:', error)
      throw error
    }
  }

  /**
   * Lista códigos de barras com paginação
   * @param {Object} params - Parâmetros de busca
   * @returns {Promise<Object>} Lista paginada de códigos
   */
  async listBarcodes(params = {}) {
    try {
      const queryParams = new URLSearchParams()

      if (params.page) queryParams.append('page', params.page)
      if (params.per_page) queryParams.append('per_page', params.per_page)
      if (params.regiao) queryParams.append('regiao', params.regiao)

      const url = `${API_BASE_URL}/codigos-barras/?${queryParams.toString()}`
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao listar códigos de barras:', error)
      throw error
    }
  }

  /**
   * Lista códigos de barras de um produto específico
   * @param {number} produtoId - ID do produto
   * @returns {Promise<Object>} Lista de códigos do produto
   */
  async listProductBarcodes(produtoId) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/produto/${produtoId}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao listar códigos do produto:', error)
      throw error
    }
  }

  /**
   * Valida formato de um código de barras
   * @param {string} code - Código a ser validado
   * @returns {Promise<Object>} Resultado da validação
   */
  async validateBarcode(code) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/validar/${code}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao validar código de barras:', error)
      throw error
    }
  }

  /**
   * Obtém estatísticas dos códigos de barras
   * @returns {Promise<Object>} Estatísticas
   */
  async getStatistics() {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/stats`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao obter estatísticas:', error)
      throw error
    }
  }

  /**
   * Deleta um código de barras
   * @param {number} id - ID do código de barras
   * @returns {Promise<boolean>} Sucesso da operação
   */
  async deleteBarcode(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/codigos-barras/${id}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success
    } catch (error) {
      console.error('Erro ao deletar código de barras:', error)
      throw error
    }
  }
}

// Instância singleton do serviço
export const barcodeService = new BarcodeService()

// Exporta também a classe para casos específicos
export default BarcodeService

