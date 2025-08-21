<template>
  <div id="app">
    <!-- Navegação Principal -->
    <nav class="main-nav">
      <div class="nav-container">
        <div class="nav-brand">
          <router-link to="/" class="brand-link">
            <span class="brand-icon">📊</span>
            <span class="brand-text">Sistema Código de Barras</span>
          </router-link>
        </div>
        
        <div class="nav-menu" :class="{ 'nav-menu-open': menuOpen }">
          <router-link to="/" class="nav-link" @click="closeMenu">
            <i class="icon">🏠</i>
            Início
          </router-link>
          
          <router-link to="/scanner" class="nav-link" @click="closeMenu">
            <i class="icon">📷</i>
            Scanner
          </router-link>
          
          <router-link to="/produtos" class="nav-link" @click="closeMenu">
            <i class="icon">📦</i>
            Produtos
          </router-link>
          
          <router-link to="/gerar" class="nav-link" @click="closeMenu">
            <i class="icon">🏷️</i>
            Gerar Código
          </router-link>
          
          <router-link to="/sobre" class="nav-link" @click="closeMenu">
            <i class="icon">ℹ️</i>
            Sobre
          </router-link>
        </div>
        
        <button class="nav-toggle" @click="toggleMenu">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <!-- Conteúdo Principal -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Rodapé -->
    <footer class="main-footer">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>Sistema Código de Barras</h3>
            <p>
              Sistema web para geração e decodificação de códigos de barras 
              baseado em CEP brasileiro com identificadores regionais.
            </p>
          </div>
          
          <div class="footer-section">
            <h4>Funcionalidades</h4>
            <ul>
              <li>Scanner via webcam</li>
              <li>Geração de códigos</li>
              <li>Consulta de CEP</li>
              <li>Download PNG</li>
            </ul>
          </div>
          
          <div class="footer-section">
            <h4>Regiões</h4>
            <ul>
              <li><strong>1:</strong> Norte/Nordeste</li>
              <li><strong>2:</strong> Centro-Oeste</li>
              <li><strong>3:</strong> Sul/Sudeste</li>
            </ul>
          </div>
          
          <div class="footer-section">
            <h4>Tecnologias</h4>
            <ul>
              <li>Vue.js 3</li>
              <li>Python Flask</li>
              <li>QuaggaJS</li>
              <li>SQLite</li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2025 Sistema de Códigos de Barras por CEP. Desenvolvido para aprendizado.</p>
        </div>
      </div>
    </footer>

    <!-- Notificações Toast -->
    <div v-if="notifications.length > 0" class="notifications">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="['notification', `notification-${notification.type}`]"
      >
        <div class="notification-content">
          <i :class="getNotificationIcon(notification.type)"></i>
          <span>{{ notification.message }}</span>
        </div>
        <button @click="removeNotification(notification.id)" class="notification-close">
          &times;
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const menuOpen = ref(false)
    const notifications = ref([])
    let notificationId = 0

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value
    }

    const closeMenu = () => {
      menuOpen.value = false
    }

    const addNotification = (message, type = 'info', duration = 5000) => {
      const id = ++notificationId
      const notification = { id, message, type }
      
      notifications.value.push(notification)
      
      if (duration > 0) {
        setTimeout(() => {
          removeNotification(id)
        }, duration)
      }
      
      return id
    }

    const removeNotification = (id) => {
      const index = notifications.value.findIndex(n => n.id === id)
      if (index > -1) {
        notifications.value.splice(index, 1)
      }
    }

    const getNotificationIcon = (type) => {
      const icons = {
        success: 'icon-success',
        error: 'icon-error',
        warning: 'icon-warning',
        info: 'icon-info'
      }
      return icons[type] || icons.info
    }

    // Disponibiliza globalmente para outros componentes
    const showNotification = (message, type = 'info', duration = 5000) => {
      return addNotification(message, type, duration)
    }

    onMounted(() => {
      // Configura notificações globais
      window.showNotification = showNotification
      
      // Verifica suporte a getUserMedia
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showNotification(
          'Seu navegador não suporta acesso à câmera. Algumas funcionalidades podem não funcionar.',
          'warning',
          10000
        )
      }
    })

    return {
      menuOpen,
      notifications,
      toggleMenu,
      closeMenu,
      removeNotification,
      getNotificationIcon,
      showNotification
    }
  }
}
</script>

<style>
/* Reset e estilos globais */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navegação */
.main-nav {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.nav-brand .brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
}

.brand-icon {
  font-size: 2rem;
}

.nav-menu {
  display: flex;
  gap: 30px;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.nav-toggle span {
  width: 25px;
  height: 3px;
  background: white;
  margin: 3px 0;
  transition: 0.3s;
  border-radius: 2px;
}

/* Conteúdo principal */
.main-content {
  flex: 1;
  min-height: calc(100vh - 70px - 200px);
}

/* Rodapé */
.main-footer {
  background: #2c3e50;
  color: white;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.footer-section h3,
.footer-section h4 {
  margin-bottom: 15px;
  color: #ecf0f1;
}

.footer-section p {
  color: #bdc3c7;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
}

.footer-section li {
  padding: 5px 0;
  color: #bdc3c7;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #34495e;
  color: #95a5a6;
}

/* Notificações */
.notifications {
  position: fixed;
  top: 90px;
  right: 20px;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.notification {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-success {
  background: #d4edda;
  border-left: 4px solid #28a745;
  color: #155724;
}

.notification-error {
  background: #f8d7da;
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.notification-warning {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  color: #856404;
}

.notification-info {
  background: #d1ecf1;
  border-left: 4px solid #17a2b8;
  color: #0c5460;
}

.notification-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.notification-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.notification-close:hover {
  opacity: 1;
}

/* Ícones das notificações */
.icon-success::before { content: "✅"; }
.icon-error::before { content: "❌"; }
.icon-warning::before { content: "⚠️"; }
.icon-info::before { content: "ℹ️"; }

/* Responsividade */
@media (max-width: 768px) {
  .nav-toggle {
    display: flex;
  }
  
  .nav-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    flex-direction: column;
    padding: 20px;
    gap: 15px;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }
  
  .nav-menu-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
  
  .nav-link {
    width: 100%;
    justify-content: center;
    padding: 15px;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .notifications {
    right: 10px;
    left: 10px;
  }
  
  .notification {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 15px;
  }
  
  .brand-text {
    display: none;
  }
  
  .footer-container {
    padding: 30px 15px 15px;
  }
}

/* Utilitários */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 1rem; }
.mt-4 { margin-top: 1.5rem; }
.mt-5 { margin-top: 3rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 1.5rem; }
.mb-5 { margin-bottom: 3rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 1rem; }
.p-4 { padding: 1.5rem; }
.p-5 { padding: 3rem; }
</style>

