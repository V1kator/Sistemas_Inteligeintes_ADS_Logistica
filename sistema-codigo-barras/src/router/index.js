import { createRouter, createWebHistory } from 'vue-router'

// Importação das views
import HomeView from '../views/HomeView.vue'
import ScannerView from '../views/ScannerView.vue'
import ProdutosView from '../views/ProdutosView.vue'
import GerarCodigoView from '../views/GerarCodigoView.vue'
import SobreView from '../views/SobreView.vue'
import ProdutoDetalhesView from '../views/ProdutoDetalhesView.vue'
import EstatisticasView from '../views/EstatisticasView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: {
      title: 'Início - Sistema Código de Barras',
      description: 'Sistema web para geração e decodificação de códigos de barras baseado em CEP'
    }
  },
  {
    path: '/scanner',
    name: 'Scanner',
    component: ScannerView,
    meta: {
      title: 'Scanner - Sistema Código de Barras',
      description: 'Scanner de códigos de barras via webcam em tempo real'
    }
  },
  {
    path: '/produtos',
    name: 'Produtos',
    component: ProdutosView,
    meta: {
      title: 'Produtos - Sistema Código de Barras',
      description: 'Gerenciamento de produtos e códigos de barras'
    }
  },
  {
    path: '/produtos/:id',
    name: 'ProdutoDetalhes',
    component: ProdutoDetalhesView,
    meta: {
      title: 'Detalhes do Produto - Sistema Código de Barras',
      description: 'Visualizar detalhes e códigos de barras do produto'
    }
  },
  {
    path: '/gerar',
    name: 'GerarCodigo',
    component: GerarCodigoView,
    meta: {
      title: 'Gerar Código - Sistema Código de Barras',
      description: 'Gerar novos códigos de barras para produtos'
    }
  },
  {
    path: '/sobre',
    name: 'Sobre',
    component: SobreView,
    meta: {
      title: 'Sobre - Sistema Código de Barras',
      description: 'Informações sobre o sistema e tecnologias utilizadas'
    }
  },
  {
    path: '/estatisticas',
    name: 'Estatisticas',
    component: EstatisticasView,
    meta: {
      title: 'Estatísticas - Sistema Código de Barras',
      description: 'Estatísticas e relatórios do sistema'
    }
  },
  // Rota 404 - deve ser a última
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
    meta: {
      title: 'Página não encontrada - Sistema Código de Barras',
      description: 'A página solicitada não foi encontrada'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Sempre rola para o topo ao navegar para uma nova rota
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Guard de navegação para atualizar meta tags
router.beforeEach((to, from, next) => {
  // Atualiza o título da página
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // Atualiza meta description
  if (to.meta.description) {
    let metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
      metaDescription.setAttribute('content', to.meta.description)
    }
  }

  // Adiciona classe CSS baseada na rota para estilos específicos
  document.body.className = `route-${to.name?.toLowerCase() || 'unknown'}`

  next()
})

// Guard após navegação para analytics ou outras ações
router.afterEach((to, from) => {
  // Aqui poderia ser adicionado Google Analytics ou outras ferramentas
  console.log(`Navegou de ${from.name || 'unknown'} para ${to.name || 'unknown'}`)
})

export default router

