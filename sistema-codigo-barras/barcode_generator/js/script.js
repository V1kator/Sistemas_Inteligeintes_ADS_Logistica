document.addEventListener('DOMContentLoaded', () => {
    const cepInput = document.getElementById('cepInput');
    const generateBarcodeBtn = document.getElementById('generateBarcodeBtn');
    const barcodeContainer = document.getElementById('barcodeContainer');
    const barcodeSvg = document.getElementById('barcode');
    const downloadBarcodeBtn = document.getElementById('downloadBarcodeBtn');
    const errorMessage = document.getElementById('errorMessage');

    // Máscara para o CEP
    cepInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, ''); // Remove tudo que não é dígito
        if (value.length > 5) {
            value = value.substring(0, 5) + '-' + value.substring(5, 8);
        }
        e.target.value = value;
    });

    generateBarcodeBtn.addEventListener('click', async () => {
        const cep = cepInput.value.replace(/\D/g, ''); // Remove o hífen para validação
        errorMessage.textContent = ''; // Limpa mensagens de erro anteriores
        barcodeSvg.innerHTML = ''; // Limpa o código de barras anterior
        downloadBarcodeBtn.style.display = 'none'; // Esconde o botão de download

        if (cep.length !== 8) {
            errorMessage.textContent = 'Por favor, digite um CEP válido com 8 dígitos.';
            return;
        }

        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();

            if (data.erro) {
                errorMessage.textContent = 'CEP não encontrado ou inválido.';
                return;
            }

            // CEP é válido, gerar código de barras
            JsBarcode(barcodeSvg, cep, {
                format: "CODE128",
                displayValue: true,
                fontSize: 18,
                height: 80,
                width: 2
            });
            downloadBarcodeBtn.style.display = 'block';

        } catch (error) {
            errorMessage.textContent = 'Erro ao validar o CEP. Tente novamente.';
            console.error('Erro:', error);
        }
    });

    downloadBarcodeBtn.addEventListener('click', () => {
        const svgData = new XMLSerializer().serializeToString(barcodeSvg);
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            const pngFile = canvas.toDataURL('image/png');
            const downloadLink = document.createElement('a');
            downloadLink.href = pngFile;
            downloadLink.download = `barcode-${cepInput.value.replace(/\D/g, '')}.png`;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        };
        img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    });
});

