import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Estilos globais
import './assets/styles/global.css'

// Configuração da aplicação
const app = createApp(App)

// Configuração do roteador
app.use(router)

// Configurações globais
// ...existing code...
app.config.globalProperties.$apiUrl = import.meta.env.VUE_APP_API_URL || 'http://localhost:5000/api'
// ...existing code...

// Propriedades globais para formatação
app.config.globalProperties.$formatCep = (cep) => {
  if (!cep) return ''
  const cleaned = cep.replace(/\D/g, '')
  if (cleaned.length === 8) {
    return `${cleaned.slice(0, 5)}-${cleaned.slice(5)}`
  }
  return cep
}

app.config.globalProperties.$formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('pt-BR')
}

app.config.globalProperties.$formatDateTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('pt-BR')
}

app.config.globalProperties.$getRegionName = (regionId) => {
  const regions = {
    1: 'Norte/Nordeste',
    2: 'Centro-Oeste',
    3: 'Sul/Sudeste'
  }
  return regions[regionId] || 'Desconhecida'
}

// Tratamento global de erros
app.config.errorHandler = (err, instance, info) => {
  console.error('Erro global da aplicação:', err)
  console.error('Informações do erro:', info)

  // Exibe notificação de erro se disponível
  if (window.showNotification) {
    window.showNotification(
      'Ocorreu um erro inesperado. Tente novamente.',
      'error',
      5000
    )
  }
}

// Configurações de desenvolvimento
if (import.meta.env.NODE_ENV === 'development') {
  app.config.devtools = true
  app.config.debug = true

  // Log de navegação em desenvolvimento
  router.afterEach((to, from) => {
    console.log(`[Router] Navegou de ${from.name || 'unknown'} para ${to.name || 'unknown'}`)
  })
}

// Monta a aplicação
app.mount('#app')

// Exporta a instância da aplicação para uso em testes
export default app

