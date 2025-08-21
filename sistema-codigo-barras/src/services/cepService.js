/**
 * Serviço para comunicação com API de CEP
 */

const API_BASE_URL = import.meta.env.VUE_APP_API_URL || 'http://localhost:5000/api'

class CepService {
  /**
   * Consulta informações de um CEP
   * @param {string} cep - CEP a ser consultado
   * @returns {Promise<Object>} Dados do CEP
   */
  async consultarCep(cep) {
    try {
      const cleanCep = this.cleanCep(cep)

      if (!this.validateCep(cleanCep)) {
        throw new Error('CEP inválido')
      }

      const response = await fetch(`${API_BASE_URL}/cep/consultar/${cleanCep}`)

      if (!response.ok) {
        if (response.status === 404) {
          return null
        }
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao consultar CEP:', error)
      throw error
    }
  }

  /**
   * Valida formato de um CEP
   * @param {string} cep - CEP a ser validado
   * @returns {Promise<Object>} Resultado da validação
   */
  async validarCep(cep) {
    try {
      const cleanCep = this.cleanCep(cep)
      const response = await fetch(`${API_BASE_URL}/cep/validar/${cleanCep}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao validar CEP:', error)
      throw error
    }
  }

  /**
   * Busca CEPs por localização
   * @param {Object} params - Parâmetros de busca
   * @returns {Promise<Object>} Resultados da busca
   */
  async buscarCeps(params) {
    try {
      const queryParams = new URLSearchParams()

      if (params.estado) queryParams.append('estado', params.estado)
      if (params.cidade) queryParams.append('cidade', params.cidade)
      if (params.logradouro) queryParams.append('logradouro', params.logradouro)
      if (params.page) queryParams.append('page', params.page)
      if (params.per_page) queryParams.append('per_page', params.per_page)

      const url = `${API_BASE_URL}/cep/buscar?${queryParams.toString()}`
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao buscar CEPs:', error)
      throw error
    }
  }

  /**
   * Formata CEP para exibição
   * @param {string} cep - CEP a ser formatado
   * @returns {Promise<Object>} CEP formatado
   */
  async formatarCep(cep) {
    try {
      const response = await fetch(`${API_BASE_URL}/cep/formatar/${cep}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao formatar CEP:', error)
      throw error
    }
  }

  /**
   * Obtém região de um CEP
   * @param {string} cep - CEP para consulta
   * @returns {Promise<Object>} Informações da região
   */
  async obterRegiaoCep(cep) {
    try {
      const cepData = await this.consultarCep(cep)

      if (!cepData || !cepData.uf) {
        return null
      }

      const response = await fetch(`${API_BASE_URL}/regioes/estado/${cepData.uf}`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao obter região do CEP:', error)
      throw error
    }
  }

  /**
   * Obtém estatísticas de CEPs
   * @returns {Promise<Object>} Estatísticas
   */
  async obterEstatisticas() {
    try {
      const response = await fetch(`${API_BASE_URL}/cep/stats`)

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success ? data.data : null
    } catch (error) {
      console.error('Erro ao obter estatísticas de CEP:', error)
      throw error
    }
  }

  /**
   * Valida formato de CEP localmente
   * @param {string} cep - CEP a ser validado
   * @returns {boolean} Se o CEP é válido
   */
  validateCep(cep) {
    if (!cep) return false
    const cleaned = this.cleanCep(cep)
    return /^\d{8}$/.test(cleaned)
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
   * Formata CEP localmente
   * @param {string} cep - CEP sem formatação
   * @returns {string} CEP formatado
   */
  formatCep(cep) {
    if (!cep) return ''
    const cleaned = this.cleanCep(cep)
    if (cleaned.length === 8) {
      return `${cleaned.slice(0, 5)}-${cleaned.slice(5)}`
    }
    return cep
  }

  /**
   * Máscara de CEP para input
   * @param {string} value - Valor atual do input
   * @returns {string} Valor com máscara aplicada
   */
  applyCepMask(value) {
    if (!value) return ''

    // Remove tudo que não é número
    const cleaned = value.replace(/\D/g, '')

    // Aplica a máscara
    if (cleaned.length <= 5) {
      return cleaned
    } else {
      return `${cleaned.slice(0, 5)}-${cleaned.slice(5, 8)}`
    }
  }

  /**
   * Obtém sugestões de CEP baseado em entrada parcial
   * @param {string} partial - CEP parcial
   * @returns {Promise<Array>} Lista de sugestões
   */
  async obterSugestoes(partial) {
    try {
      if (!partial || partial.length < 3) {
        return []
      }

      const cleaned = this.cleanCep(partial)
      const response = await fetch(`${API_BASE_URL}/cep/sugestoes/${cleaned}`)

      if (!response.ok) {
        return []
      }

      const data = await response.json()
      return data.success ? data.data : []
    } catch (error) {
      console.error('Erro ao obter sugestões de CEP:', error)
      return []
    }
  }

  /**
   * Verifica se CEP está em cache
   * @param {string} cep - CEP a ser verificado
   * @returns {Promise<boolean>} Se está em cache
   */
  async verificarCache(cep) {
    try {
      const cleanCep = this.cleanCep(cep)
      const response = await fetch(`${API_BASE_URL}/cep/cache/${cleanCep}`)

      if (!response.ok) {
        return false
      }

      const data = await response.json()
      return data.success && data.data.em_cache
    } catch (error) {
      console.error('Erro ao verificar cache de CEP:', error)
      return false
    }
  }

  /**
   * Limpa cache de CEPs
   * @returns {Promise<boolean>} Sucesso da operação
   */
  async limparCache() {
    try {
      const response = await fetch(`${API_BASE_URL}/cep/cache`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.status}`)
      }

      const data = await response.json()
      return data.success
    } catch (error) {
      console.error('Erro ao limpar cache de CEP:', error)
      throw error
    }
  }
}

// Instância singleton do serviço
export const cepService = new CepService()

// Exporta também a classe para casos específicos
export default CepService

