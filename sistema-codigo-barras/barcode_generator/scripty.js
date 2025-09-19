let currentQRCode = null;
let videoStream = null;

function gerarQRCode() {
    const cepInput = document.getElementById('cep');
    const cep = cepInput.value.replace(/\D/g, '');
    const qrcodeDiv = document.getElementById('qrcode');
    const addressDiv = document.getElementById('address');
    const errorDiv = document.getElementById('errorMessage');
    const downloadBtn = document.getElementById('downloadBtn');

    // Limpa resultados anteriores
    qrcodeDiv.innerHTML = '';
    addressDiv.innerHTML = '';
    errorDiv.style.display = 'none';
    downloadBtn.style.display = 'none';

    // Validação do CEP
    if (cep.length !== 8) {
        errorDiv.textContent = 'CEP inválido! Digite 8 números.';
        errorDiv.style.display = 'block';
        return;
    }

    // Consulta ViaCEP
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                throw new Error('CEP não encontrado');
            }

            // Exibe informações de endereço
            addressDiv.innerHTML = `
                        <h3>Endereço:</h3>
                        <p>${data.logradouro || 'Não informado'}</p>
                        <p>${data.bairro || 'Não informado'}</p>
                        <p>${data.localidade} - ${data.uf}</p>
                    `;

            // Gera QR Code com o CEP (apenas números)
            if (currentQRCode) {
                currentQRCode.clear();
            }

            currentQRCode = new QRCode(qrcodeDiv, {
                text: data.cep.replace('-', ''), // Apenas o CEP numérico
                width: 200,
                height: 200
            });

            // Mostra botão de download
            downloadBtn.style.display = 'block';
        })
        .catch(error => {
            errorDiv.textContent = `Erro: ${error.message}`;
            errorDiv.style.display = 'block';
        });
}

function downloadQRCode() {
    const canvas = document.querySelector('#qrcode canvas');
    if (!canvas) return;

    // Cria link de download
    const link = document.createElement('a');
    link.download = `qrcode-cep-${document.getElementById('cep').value.replace(/\D/g, '')}.png`;
    link.href = canvas.toDataURL('image/png');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Formatação automática do CEP (opcional)
document.getElementById('cep').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 5) {
        value = value.substring(0, 5) + '-' + value.substring(5, 8);
    }
    e.target.value = value;
});

// Elementos para leitura de QR Code
const video = document.getElementById('video');
const videoContainer = document.getElementById('videoContainer');
const scanButton = document.getElementById('scanButton');
const stopButton = document.getElementById('stopButton');

function startScan() {
    // Esconder outros elementos
    document.getElementById('qrcode').innerHTML = '';
    document.getElementById('address').innerHTML = '';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('downloadBtn').style.display = 'none';

    // Mostrar o vídeo
    videoContainer.style.display = 'block';
    stopButton.style.display = 'inline-block';
    scanButton.style.display = 'none';

    // Solicitar acesso à câmera
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(function (stream) {
            videoStream = stream;
            video.srcObject = stream;
            video.play();
            requestAnimationFrame(tick);
        })
        .catch(function (err) {
            alert("Erro ao acessar a câmera: " + err);
            stopScan();
        });
}

function stopScan() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        videoStream = null;
    }
    videoContainer.style.display = 'none';
    stopButton.style.display = 'none';
    scanButton.style.display = 'inline-block';
}

function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert",
        });

        if (code) {
            // Encontrou um QR Code
            stopScan();
            buscarEndereco(code.data);
        } else {
            requestAnimationFrame(tick);
        }
    } else {
        requestAnimationFrame(tick);
    }
}



function buscarEndereco(cep) {
    const cepNumerico = cep.replace(/\D/g, '');
    const addressDiv = document.getElementById('address');
    const errorDiv = document.getElementById('errorMessage');

    // Limpa resultados anteriores
    addressDiv.innerHTML = '';
    errorDiv.style.display = 'none';

    // Validação do CEP
    if (cepNumerico.length !== 8) {
        errorDiv.textContent = 'CEP inválido no QR Code!';
        errorDiv.style.display = 'block';
        return;
    }

    // Consulta ViaCEP
    fetch(`https://viacep.com.br/ws/${cepNumerico}/json/`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                throw new Error('CEP não encontrado');
            }

            var ponto_de_entrega = data.uf;

            // Lógica do ponto de entrega baseado na UF
            const norteNordeste = ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO', 'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'];
            const sulSudeste = ['SP', 'RJ', 'MG', 'ES', 'PR', 'SC', 'RS'];
            const centroOeste = ['DF', 'GO', 'MT', 'MS'];

            if (norteNordeste.includes(ponto_de_entrega)) {
                ponto_de_entrega = 1; // Norte e Nordeste
            } else if (sulSudeste.includes(ponto_de_entrega)) {
                ponto_de_entrega = 2; // Sul e Sudeste
            } else if (centroOeste.includes(ponto_de_entrega)) {
                ponto_de_entrega = 3; // Centro-Oeste
            } else {
                ponto_de_entrega = 0; // UF não mapeada
            }

            // Envia o ponto de entrega para o Arduino
            enviarParaArduino(ponto_de_entrega);



            // Exibe informações de endereço
            addressDiv.innerHTML = `
                        <h3>Endereço a partir do QR Code:</h3>
                        <p>${data.logradouro || 'Não informado'}</p>
                        <p>${data.bairro || 'Não informado'}</p>
                        <p>${data.localidade} - ${data.uf}</p>
                        <p>CEP: ${data.cep}</p>
                        <div class="ponto-entrega">Ponto de Entrega: ${ponto_de_entrega}</div>
                    `;
        })
        .catch(error => {
            errorDiv.textContent = `Erro: ${error.message}`;
            errorDiv.style.display = 'block';
        });
}


async function enviarParaArduino(ponto_de_entrega) {
    try {
        // Pede ao usuário para escolher a porta do Arduino
        const port = await navigator.serial.requestPort();
        await port.open({ baudRate: 9600 });

        const encoder = new TextEncoderStream();
        const outputDone = encoder.readable.pipeTo(port.writable);
        const writer = encoder.writable.getWriter();

        // Envia o ponto de entrega
        await writer.write(ponto_de_entrega.toString() + "\n");

        // Libera a porta
        writer.releaseLock();
        await outputDone;
    } catch (err) {
        console.error("Erro ao enviar para Arduino:", err);
    }
}
