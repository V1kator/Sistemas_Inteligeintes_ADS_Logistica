document.addEventListener("DOMContentLoaded", () => {
    const scannerContainer = document.getElementById("interactive");
    const startScannerBtn = document.getElementById("startScannerBtn");
    const stopScannerBtn = document.getElementById("stopScannerBtn");
    const scannedCepResult = document.getElementById("scannedCepResult");
    const scannedAddressResult = document.getElementById("scannedAddressResult");
    const deliveryPointResult = document.getElementById("deliveryPointResult");

    let scannerRunning = false;

    startScannerBtn.addEventListener("click", () => {
        if (!scannerRunning) {
            startScanner();
        }
    });

    stopScannerBtn.addEventListener("click", () => {
        if (scannerRunning) {
            stopScanner();
        }
    });

    function startScanner() {
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: scannerContainer, // Usar o container em vez do elemento video
                constraints: {
                    width: 640,
                    height: 480,
                    facingMode: "environment" // ou "user" para câmera frontal
                }
            },
            locator: {
                patchSize: "medium",
                halfSample: true
            },
            numOfWorkers: 2,
            decoder: {
                readers: ["code_128_reader", "ean_reader", "ean_8_reader", "code_39_reader", "code_39_vin_reader", "codabar_reader", "upc_reader", "upc_e_reader", "i2of5_reader"]
            },
            locate: true
        }, function (err) {
            if (err) {
                console.error(err);
                scannedCepResult.textContent = `Erro ao iniciar o scanner: ${err.message}`;
                return;
            }
            console.log("Initialization finished. Ready to start");
            Quagga.start();
            scannerRunning = true;
            scannedCepResult.textContent = "Scanner iniciado. Aponte para um código de barras.";
            scannedAddressResult.innerHTML = "";
            deliveryPointResult.innerHTML = ""; // Limpa o ponto de entrega anterior
            startScannerBtn.style.display = "none";
            stopScannerBtn.style.display = "block";
        });

        Quagga.onDetected(function (result) {
            const code = result.codeResult.code;
            console.log("Barcode detected and processed: ", code);
            // Tenta extrair o CEP do código de barras
            const cepMatch = code.match(/\d{8}/); // Procura por 8 dígitos consecutivos
            if (cepMatch) {
                const cep = cepMatch[0];
                scannedCepResult.textContent = `CEP detectado: ${cep.substring(0, 5)}-${cep.substring(5, 8)}`;
                fetchAddressByCep(cep);
                stopScanner(); // Para o scanner após detectar um CEP
            } else {
                scannedCepResult.textContent = `Código de barras detectado, mas CEP não encontrado: ${code}`;
            }
        });

        Quagga.onProcessed(function (result) {
            const drawingCtx = Quagga.canvas.ctx.overlay;
            const drawingCanvas = Quagga.canvas.dom.overlay;

            if (result) {
                if (result.boxes) {
                    drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.width), parseInt(drawingCanvas.height));
                    result.boxes.filter(function (box) {
                        return box !== result.box;
                    }).forEach(function (box) {
                        Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, { color: "green", lineWidth: 2 });
                    });
                }

                if (result.box) {
                    Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, { color: "#00F", lineWidth: 2 });
                }

                if (result.codeResult && result.codeResult.code) {
                    Quagga.ImageDebug.drawPath(result.line, { x: "x", y: "y" }, drawingCtx, { color: "red", lineWidth: 3 });
                }
            }
        });
    }

    function stopScanner() {
        Quagga.stop();
        scannerRunning = false;
        scannedCepResult.textContent = "Scanner parado.";
        startScannerBtn.style.display = "block";
        stopScannerBtn.style.display = "none";
    }

    async function fetchAddressByCep(cep) {
        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();

            if (data.erro) {
                scannedAddressResult.innerHTML = 
                    `<p class="error-message">Não foi possível encontrar o endereço para o CEP ${cep}.</p>`;
                deliveryPointResult.innerHTML = "";
                return;
            }

            scannedAddressResult.innerHTML = `
                <p><strong>Logradouro:</strong> ${data.logradouro}</p>
                <p><strong>Bairro:</strong> ${data.bairro}</p>
                <p><strong>Localidade:</strong> ${data.localidade}</p>
                <p><strong>Estado:</strong> ${data.uf}</p>
                <p><strong>DDD:</strong> ${data.ddd}</p>
            `;

            const deliveryPoint = getDeliveryPoint(data.uf);
            deliveryPointResult.innerHTML = `<p><strong>Ponto de Entrega:</strong> ${deliveryPoint}</p>`;

            // Enviar o ponto de entrega para o servidor Flask
            sendDeliveryPointToEV3(deliveryPoint);

        } catch (error) {
            scannedAddressResult.innerHTML = 
                `<p class="error-message">Erro ao buscar endereço: ${error.message}</p>`;
            deliveryPointResult.innerHTML = "";
            console.error("Erro ao buscar endereço:", error);
        }
    }

    async function sendDeliveryPointToEV3(deliveryPoint) {
        try {
            const response = await fetch("http://localhost:5000/api/control_ev3", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ delivery_point: deliveryPoint })
            });
            const result = await response.json();
            if (result.success) {
                console.log("Comando enviado ao EV3 com sucesso:", result.message);
            } else {
                console.error("Erro ao enviar comando ao EV3:", result.message);
            }
        } catch (error) {
            console.error("Erro de comunicação com o servidor EV3:", error);
        }
    }

    function getDeliveryPoint(uf) {
        const ufLower = uf.toLowerCase();
        if (["ac", "ap", "am", "pa", "ro", "rr", "to", "al", "ba", "ce", "ma", "pb", "pe", "pi", "rn", "se"].includes(ufLower)) {
            return 1; // Norte e Nordeste
        } else if (["es", "mg", "rj", "sp", "pr", "rs", "sc"].includes(ufLower)) {
            return 2; // Sul e Sudeste
        } else if (["df", "go", "mt", "ms"].includes(ufLower)) {
            return 3; // Centro-Oeste
        } else {
            return "Não classificado";
        }
    }

    // Expor fetchAddressByCep e sendDeliveryPointToEV3 para testes no console
    window.fetchAddressByCep = fetchAddressByCep;
    window.sendDeliveryPointToEV3 = sendDeliveryPointToEV3;

    // Função para simular a detecção de um código de barras para testes
    window.simulateBarcodeDetection = (cep) => {
        const mockResult = {
            codeResult: {
                code: cep + "00000" // Adiciona alguns dígitos para simular um código de barras real
            }
        };
        // Chamamos diretamente a função onDetected do Quagga com o mockResult
        // Isso simula o que aconteceria se o Quagga detectasse um código de barras
        Quagga.onDetected(mockResult);
    };
});

