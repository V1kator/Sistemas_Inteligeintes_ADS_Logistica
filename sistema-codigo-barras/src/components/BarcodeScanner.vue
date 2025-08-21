<template>
  <div class="barcode-scanner">
    <div class="scanner-header">
      <h2>Scanner de Códigos de Barras</h2>
      <p>Aponte a câmera para um código de barras para decodificar</p>
    </div>

    <!-- Controles do Scanner -->
    <div class="scanner-controls">
      <button 
        @click="startScanner" 
        :disabled="isScanning"
        class="btn btn-primary"
      >
        <i class="icon-play"></i>
        Iniciar Scanner
      </button>
      
      <button 
        @click="stopScanner" 
        :disabled="!isScanning"
        class="btn btn-secondary"
      >
        <i class="icon-stop"></i>
        Parar Scanner
      </button>

      <select v-model="selectedCamera" @change="changeCamera" :disabled="!isScanning">
        <option value="">Selecionar Câmera</option>
        <option 
          v-for="camera in availableCameras" 
          :key="camera.deviceId" 
          :value="camera.deviceId"
        >
          {{ camera.label || `Câmera ${camera.deviceId.substring(0, 8)}` }}
        </option>
      </select>
    </div>

    <!-- Área do Scanner -->
    <div class="scanner-container" v-show="isScanning">
      <div id="scanner-viewport" class="viewport">
        <!-- QuaggaJS será renderizado aqui -->
      </div>
      
      <div class="scanner-overlay">
        <div class="scan-line"></div>
        <div class="corner top-left"></div>
        <div class="corner top-right"></div>
        <div class="corner bottom-left"></div>
        <div class="corner bottom-right"></div>
      </div>
    </div>

    <!-- Status do Scanner -->
    <div class="scanner-status">
      <div v-if="isScanning" class="status-item scanning">
        <i class="icon-camera"></i>
        <span>Scanner ativo - Aguardando código...</span>
      </div>
      
      <div v-if="lastError" class="status-item error">
        <i class="icon-alert"></i>
        <span>{{ lastError }}</span>
      </div>
    </div>

    <!-- Resultados -->
    <div v-if="detectedCodes.length > 0" class="results-section">
      <h3>Códigos Detectados</h3>
      <div class="results-list">
        <div 
          v-for="(result, index) in detectedCodes" 
          :key="index"
          class="result-item"
          @click="searchProduct(result.code)"
        >
          <div class="result-image">
            <img :src="result.image" alt="Código detectado" />
          </div>
          <div class="result-info">
            <h4>{{ result.code }}</h4>
            <p>{{ result.timestamp }}</p>
            <button class="btn btn-sm btn-primary">
              Buscar Produto
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Produto Encontrado -->
    <div v-if="foundProduct" class="modal-overlay" @click="closeProductModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Produto Encontrado</h3>
          <button @click="closeProductModal" class="btn-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="product-info">
            <h4>{{ foundProduct.produto.nome }}</h4>
            <p><strong>CEP:</strong> {{ foundProduct.produto.cep_formatado }}</p>
            <p><strong>Estado:</strong> {{ foundProduct.produto.estado }}</p>
            <p><strong>Cidade:</strong> {{ foundProduct.produto.cidade }}</p>
            <p><strong>Região:</strong> {{ getRegionName(foundProduct.regiao_identificador) }}</p>
            <p><strong>Código:</strong> {{ foundProduct.codigo_completo }}</p>
          </div>
          
          <div class="product-actions">
            <button 
              @click="downloadBarcode(foundProduct.id)" 
              class="btn btn-primary"
            >
              <i class="icon-download"></i>
              Baixar Código PNG
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { barcodeService } from '../services/barcodeService'

export default {
  name: 'BarcodeScanner',
  setup() {
    // Estados reativos
    const isScanning = ref(false)
    const lastError = ref('')
    const detectedCodes = ref([])
    const availableCameras = ref([])
    const selectedCamera = ref('')
    const foundProduct = ref(null)

    // Configuração do QuaggaJS
    const quaggaConfig = {
      inputStream: {
        type: "LiveStream",
        target: document.querySelector('#scanner-viewport'),
        constraints: {
          width: { min: 640 },
          height: { min: 480 },
          aspectRatio: { min: 1, max: 100 },
          facingMode: "environment"
        }
      },
      locator: {
        patchSize: "medium",
        halfSample: true
      },
      numOfWorkers: 2,
      frequency: 10,
      decoder: {
        readers: [{
          format: "code_128_reader",
          config: {}
        }]
      },
      locate: true
    }

    // Métodos
    const startScanner = async () => {
      try {
        lastError.value = ''
        
        // Aguarda o DOM estar pronto
        await new Promise(resolve => setTimeout(resolve, 100))
        
        // Configura target do scanner
        quaggaConfig.inputStream.target = document.querySelector('#scanner-viewport')
        
        if (selectedCamera.value) {
          quaggaConfig.inputStream.constraints.deviceId = selectedCamera.value
        }

        // Inicializa QuaggaJS
        window.Quagga.init(quaggaConfig, (err) => {
          if (err) {
            console.error('Erro ao inicializar scanner:', err)
            lastError.value = 'Erro ao acessar câmera: ' + err.message
            return
          }
          
          isScanning.value = true
          window.Quagga.start()
          
          // Configura eventos
          setupQuaggaEvents()
        })
        
      } catch (error) {
        console.error('Erro ao iniciar scanner:', error)
        lastError.value = 'Erro ao iniciar scanner: ' + error.message
      }
    }

    const stopScanner = () => {
      if (window.Quagga) {
        window.Quagga.stop()
        window.Quagga.offDetected()
        window.Quagga.offProcessed()
      }
      isScanning.value = false
    }

    const setupQuaggaEvents = () => {
      // Evento quando código é detectado
      window.Quagga.onDetected((result) => {
        const code = result.codeResult.code
        const canvas = window.Quagga.canvas.dom.image
        
        // Evita códigos duplicados
        if (!detectedCodes.value.find(item => item.code === code)) {
          detectedCodes.value.unshift({
            code: code,
            image: canvas.toDataURL(),
            timestamp: new Date().toLocaleString('pt-BR')
          })
          
          // Mantém apenas os últimos 10 códigos
          if (detectedCodes.value.length > 10) {
            detectedCodes.value = detectedCodes.value.slice(0, 10)
          }
        }
      })

      // Evento para desenhar overlay
      window.Quagga.onProcessed((result) => {
        const drawingCtx = window.Quagga.canvas.ctx.overlay
        const drawingCanvas = window.Quagga.canvas.dom.overlay

        if (result) {
          if (result.boxes) {
            drawingCtx.clearRect(0, 0, 
              parseInt(drawingCanvas.getAttribute("width")), 
              parseInt(drawingCanvas.getAttribute("height"))
            )
            
            result.boxes.filter(box => box !== result.box).forEach(box => {
              window.Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx, {
                color: "green", 
                lineWidth: 2
              })
            })
          }

          if (result.box) {
            window.Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx, {
              color: "#00F", 
              lineWidth: 2
            })
          }

          if (result.codeResult && result.codeResult.code) {
            window.Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx, {
              color: 'red', 
              lineWidth: 3
            })
          }
        }
      })
    }

    const loadCameras = async () => {
      try {
        if (window.Quagga && window.Quagga.CameraAccess) {
          const devices = await window.Quagga.CameraAccess.enumerateVideoDevices()
          availableCameras.value = devices
        }
      } catch (error) {
        console.error('Erro ao carregar câmeras:', error)
      }
    }

    const changeCamera = () => {
      if (isScanning.value) {
        stopScanner()
        setTimeout(startScanner, 500)
      }
    }

    const searchProduct = async (code) => {
      try {
        const product = await barcodeService.searchByCode(code)
        if (product) {
          foundProduct.value = product
        } else {
          lastError.value = 'Produto não encontrado para o código: ' + code
        }
      } catch (error) {
        console.error('Erro ao buscar produto:', error)
        lastError.value = 'Erro ao buscar produto: ' + error.message
      }
    }

    const downloadBarcode = async (barcodeId) => {
      try {
        await barcodeService.downloadBarcode(barcodeId)
      } catch (error) {
        console.error('Erro ao baixar código:', error)
        lastError.value = 'Erro ao baixar código: ' + error.message
      }
    }

    const closeProductModal = () => {
      foundProduct.value = null
    }

    const getRegionName = (regionId) => {
      const regions = {
        1: 'Norte/Nordeste',
        2: 'Centro-Oeste', 
        3: 'Sul/Sudeste'
      }
      return regions[regionId] || 'Desconhecida'
    }

    // Lifecycle hooks
    onMounted(() => {
      // Carrega script do QuaggaJS se não estiver disponível
      if (!window.Quagga) {
        const script = document.createElement('script')
        script.src = 'https://serratus.github.io/quaggaJS/examples/js/quagga.min.js'
        script.onload = () => {
          loadCameras()
        }
        document.head.appendChild(script)
      } else {
        loadCameras()
      }
    })

    onUnmounted(() => {
      stopScanner()
    })

    return {
      isScanning,
      lastError,
      detectedCodes,
      availableCameras,
      selectedCamera,
      foundProduct,
      startScanner,
      stopScanner,
      changeCamera,
      searchProduct,
      downloadBarcode,
      closeProductModal,
      getRegionName
    }
  }
}
</script>

<style scoped>
.barcode-scanner {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.scanner-header {
  text-align: center;
  margin-bottom: 20px;
}

.scanner-header h2 {
  color: #333;
  margin-bottom: 10px;
}

.scanner-controls {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #545b62;
}

.scanner-container {
  position: relative;
  background: #000;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}

#scanner-viewport {
  width: 100%;
  height: 400px;
  position: relative;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.scan-line {
  position: absolute;
  top: 50%;
  left: 10%;
  right: 10%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #ff0000, transparent);
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

.corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 3px solid #00ff00;
}

.corner.top-left {
  top: 20px;
  left: 20px;
  border-right: none;
  border-bottom: none;
}

.corner.top-right {
  top: 20px;
  right: 20px;
  border-left: none;
  border-bottom: none;
}

.corner.bottom-left {
  bottom: 20px;
  left: 20px;
  border-right: none;
  border-top: none;
}

.corner.bottom-right {
  bottom: 20px;
  right: 20px;
  border-left: none;
  border-top: none;
}

.scanner-status {
  margin-bottom: 20px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.status-item.scanning {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-item.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.results-section {
  margin-top: 30px;
}

.results-list {
  display: grid;
  gap: 15px;
}

.result-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.result-item:hover {
  background: #f8f9fa;
  border-color: #007bff;
}

.result-image img {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.result-info {
  flex: 1;
}

.result-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.result-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.product-info {
  margin-bottom: 20px;
}

.product-info h4 {
  color: #333;
  margin-bottom: 15px;
}

.product-info p {
  margin: 8px 0;
  color: #666;
}

.product-actions {
  text-align: center;
}

select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  min-width: 200px;
}

@media (max-width: 768px) {
  .scanner-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .result-item {
    flex-direction: column;
  }
  
  .result-image {
    text-align: center;
  }
}
</style>

