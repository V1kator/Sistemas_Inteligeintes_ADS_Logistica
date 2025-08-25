# Guia de Teste do Projeto Gerador e Scanner de Código de Barras com Integração LEGO EV3

Este guia detalha os passos necessários para configurar e testar o projeto completo em um ambiente Windows 11, utilizando o Visual Studio Code como editor de código. Ele aborda a execução do frontend (site), do backend (servidor Flask) e a integração com um simulador do LEGO EV3, além de instruções para conexão com um EV3 real.

## 1. Introdução

O projeto consiste em um site web que permite gerar códigos de barras a partir de CEPs e escanear códigos de barras para extrair CEPs e dados de endereço. A funcionalidade mais recente adicionada é a categorização do CEP em um "ponto de entrega" (1, 2 ou 3) e o envio dessa informação para um servidor intermediário, que, por sua vez, controlaria um seletor em uma esteira LEGO EV3.

Este guia irá ajudá-lo a:

*   Configurar o ambiente de desenvolvimento no Windows 11.
*   Executar o servidor Flask (backend) que simula a comunicação com o LEGO EV3.
*   Abrir e interagir com o site (frontend).
*   Testar a comunicação entre o site e o servidor.
*   Entender como seria a conexão com um LEGO EV3 real.




## 2. Pré-requisitos

Antes de iniciar, certifique-se de que você tem os seguintes softwares instalados em seu sistema Windows 11:

*   **Visual Studio Code (VS Code)**: Um editor de código-fonte leve e poderoso. Se você ainda não o tem, pode baixá-lo em [https://code.visualstudio.com/](https://code.visualstudio.com/).
*   **Python 3.x**: O servidor intermediário é desenvolvido em Python. Recomenda-se a versão 3.8 ou superior. Você pode baixá-lo em [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/). Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.
*   **Git (Opcional, mas recomendado)**: Para gerenciar versões e clonar repositórios. Baixe em [https://git-scm.com/download/win](https://git-scm.com/download/win).
*   **Node.js e npm (Opcional, para desenvolvimento frontend avançado)**: Embora o frontend seja em HTML/CSS/JS puro, ter o Node.js pode ser útil para futuras extensões ou para gerenciar dependências JavaScript. Baixe em [https://nodejs.org/en/download/](https://nodejs.org/en/download/).




## 3. Configuração dos Arquivos do Projeto

Você recebeu um arquivo `projeto_completo.zip` que contém todos os arquivos necessários do projeto. Siga os passos abaixo para configurá-lo:

1.  **Extraia o arquivo ZIP**: Descompacte o `projeto_completo.zip` em um local de sua preferência no seu computador (ex: `C:\Projetos\`). Isso criará uma pasta `projeto_completo` com a seguinte estrutura:

    ```
    projeto_completo/
    ├── barcode_generator/           # Site frontend (HTML, CSS, JS)
    │   ├── css/
    │   ├── js/
    │   └── index.html
    ├── ev3_controller/             # Servidor backend (Python/Flask)
    │   ├── src/
    │   │   ├── main.py
    │   │   └── routes/
    │   │       └── ev3_control.py
    │   └── requirements.txt
    ├── solution_proposal.md       # Documentação da solução
    ├── ev3_research_findings.md   # Pesquisa sobre EV3
    └── todo.md                   # Progresso do projeto
    ```

2.  **Abra o projeto no VS Code**: Abra o Visual Studio Code e vá em `File > Open Folder...` (ou `Arquivo > Abrir Pasta...`) e selecione a pasta `projeto_completo` que você acabou de extrair.




## 4. Configuração e Execução do Servidor Flask (Backend)

O servidor Flask é responsável por receber as requisições do frontend e simular (ou, em um ambiente real, controlar) o LEGO EV3. Siga os passos abaixo para configurá-lo e executá-lo:

1.  **Abra o Terminal no VS Code**: No VS Code, vá em `Terminal > New Terminal` (ou `Terminal > Novo Terminal`). Certifique-se de que o terminal está no diretório raiz do projeto (`projeto_completo`).

2.  **Navegue até a pasta do servidor**: Digite o seguinte comando no terminal e pressione Enter:

    ```bash
    cd ev3_controller
    ```

3.  **Crie um Ambiente Virtual (Recomendado)**: É uma boa prática isolar as dependências do projeto. Execute os comandos:

    ```bash
    python -m venv venv
    ```

4.  **Ative o Ambiente Virtual**: 

    *   **No PowerShell (Windows)**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   **No Git Bash ou WSL (Windows)**:
        ```bash
        source venv/Scripts/activate
        ```

    Você saberá que o ambiente virtual está ativo quando `(venv)` aparecer no início da linha de comando do seu terminal.

5.  **Instale as Dependências**: Com o ambiente virtual ativado, instale as bibliotecas Python necessárias. O arquivo `requirements.txt` lista todas elas.

    ```bash
    pip install -r requirements.txt
    ```

6.  **Execute o Servidor Flask**: Agora você pode iniciar o servidor. Ele será executado em modo de simulação, pois a biblioteca `ev3dev2` não estará disponível no seu Windows 11.

    ```bash
    python src/main.py
    ```

    Você deverá ver uma saída no terminal indicando que o servidor Flask está rodando, algo como:

    ```
     * Serving Flask app 'main'
     * Debug mode: on
    WARNING:root:Biblioteca ev3dev2 não encontrada. Executando em modo simulação.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5000
     * Running on http://<seu_ip_local>:5000
    ```

    Mantenha este terminal aberto e o servidor rodando enquanto estiver testando o frontend.




## 5. Teste do Frontend (Site)

O frontend é um site estático em HTML, CSS e JavaScript. Para testá-lo, basta abrir o arquivo `index.html` no seu navegador web preferido (Google Chrome, Firefox, Edge, etc.).

1.  **Localize o arquivo `index.html`**: No VS Code, navegue até a pasta `barcode_generator` e localize o arquivo `index.html`.

2.  **Abra no Navegador**: Clique com o botão direito do mouse no arquivo `index.html` e selecione `Reveal in File Explorer` (ou `Revelar no Explorador de Arquivos`). Em seguida, clique duas vezes no arquivo `index.html` para abri-lo no seu navegador padrão.

    Alternativamente, você pode copiar o caminho completo do arquivo (`C:\Projetos\projeto_completo\barcode_generator\index.html`) e colá-lo diretamente na barra de endereços do seu navegador.

3.  **Verifique a Interface**: Você deverá ver a interface do gerador e scanner de código de barras. Verifique se todos os elementos visuais estão corretos e se a funcionalidade de geração de código de barras (digitando um CEP e clicando em "Gerar Código de Barras") ainda funciona.




## 6. Teste da Comunicação Frontend-Backend e Simulação do LEGO EV3

Com o servidor Flask rodando em um terminal do VS Code e o site aberto no seu navegador, você pode testar a comunicação entre eles e observar a simulação do controle do LEGO EV3.

1.  **Inicie o Scanner no Frontend**: No site aberto no navegador, role a página para baixo até a seção "Scanner de Código de Barras" e clique no botão "Iniciar Scanner".

    *   **Permissão da Câmera**: O navegador pedirá permissão para acessar sua webcam. **Permita o acesso** para que o scanner possa funcionar.
    *   **Visualização da Câmera**: Você deverá ver a imagem da sua webcam na área preta do scanner. Se a tela continuar preta, verifique se a permissão da câmera foi concedida e se não há outro aplicativo usando a câmera.

2.  **Simule a Detecção de um Código de Barras**: Como você provavelmente não terá um código de barras físico com um CEP para escanear imediatamente, você pode simular a detecção usando o console do navegador. Isso enviará um CEP para o frontend, que por sua vez o enviará para o backend.

    *   **Abra o Console do Desenvolvedor**: No navegador, pressione `F12` para abrir as Ferramentas do Desenvolvedor. Vá para a aba `Console`.

    *   **Execute o Comando de Simulação**: Digite um dos seguintes comandos no console e pressione Enter. Cada CEP corresponde a uma região diferente e, consequentemente, a um "ponto de entrega" diferente:

        *   **CEP para Ponto de Entrega 1 (Norte/Nordeste)**:
            ```javascript
            window.simulateBarcodeDetection("69000000"); // Exemplo: Manaus, AM
            ```
        *   **CEP para Ponto de Entrega 2 (Sul/Sudeste)**:
            ```javascript
            window.simulateBarcodeDetection("01310100"); // Exemplo: São Paulo, SP
            ```
        *   **CEP para Ponto de Entrega 3 (Centro-Oeste)**:
            ```javascript
            window.simulateBarcodeDetection("70000000"); // Exemplo: Brasília, DF
            ```

3.  **Observe o Frontend**: Após executar o comando de simulação, você deverá ver no site:

    *   O CEP detectado e formatado.
    *   Os dados do endereço (Logradouro, Bairro, Localidade, Estado, DDD) buscados via ViaCEP.
    *   O "Ponto de Entrega" categorizado (1, 2 ou 3) com base no estado.

4.  **Observe o Terminal do Servidor Flask**: Volte para o terminal do VS Code onde o servidor Flask está rodando. Você deverá ver mensagens de log indicando que o servidor recebeu a requisição do frontend e qual "ponto de entrega" foi recebido. Por exemplo:

    ```
    INFO:werkzeug:127.0.0.1 - - [23/Aug/2025 19:30:00] "POST /api/control_ev3 HTTP/1.1" 200 -
    INFO:root:Comando recebido para Ponto de Entrega: 1. Simulando movimento do motor para -90 graus.
    ```

    A mensagem `WARNING:root:Biblioteca ev3dev2 não encontrada. Executando em modo simulação.` é esperada, pois você não tem um LEGO EV3 real conectado. O servidor está simulando o movimento do motor.

5.  **Teste os Diferentes Pontos de Entrega**: Repita o passo 2 e 3 para os diferentes CEPs de simulação (Ponto 1, Ponto 2, Ponto 3) e observe as saídas correspondentes no frontend e no terminal do servidor.




## 7. Conexão com um LEGO EV3 Real (Opcional)

Se você possui um LEGO EV3 e deseja testar a funcionalidade física, siga estes passos. Este processo requer que seu LEGO EV3 esteja configurado com o sistema operacional `ev3dev` e conectado à mesma rede Wi-Fi que o computador onde o servidor Flask está rodando.

### 7.1. Pré-requisitos para LEGO EV3 Real

*   **LEGO Mindstorms EV3 Brick**: Com firmware `ev3dev` instalado. Você pode encontrar instruções e downloads em [https://www.ev3dev.org/](https://www.ev3dev.org/).
*   **Adaptador Wi-Fi compatível com EV3**: Para conectar o EV3 à sua rede sem fio.
*   **Motor Grande LEGO EV3**: Conectado à porta `A` do seu EV3.

### 7.2. Configuração do EV3

1.  **Conecte o EV3 à Rede Wi-Fi**: Siga as instruções da documentação do `ev3dev` para conectar seu EV3 à sua rede Wi-Fi. Anote o endereço IP do seu EV3.

2.  **Instale `python-ev3dev` no EV3**: Conecte-se ao seu EV3 via SSH (usando o terminal do VS Code ou PuTTY) e instale a biblioteca `python-ev3dev`:

    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install python-ev3dev
    ```

### 7.3. Executando o Servidor no Computador (Conectado ao EV3)

Para que o servidor Flask possa se comunicar com o EV3 real, ele precisa ser executado em um computador que esteja na mesma rede que o EV3. O servidor Flask que você configurou na Seção 4 já está pronto para isso.

1.  **Certifique-se de que o servidor Flask está rodando**: Siga os passos da Seção 4 para iniciar o servidor Flask no seu computador.

2.  **Verifique a Conectividade**: No terminal onde o servidor Flask está rodando, você pode tentar "pingar" o EV3 para verificar a conectividade de rede:

    ```bash
    ping <endereço_IP_do_seu_EV3>
    ```

    Se o ping for bem-sucedido, a comunicação de rede está funcionando.

### 7.4. Testando a Integração com o EV3 Real

Com o servidor Flask rodando no seu computador e o EV3 conectado e configurado, você pode testar a integração:

1.  **Abra o Site no Navegador**: Abra o `index.html` conforme a Seção 5.

2.  **Simule a Detecção de um Código de Barras**: Use os comandos `window.simulateBarcodeDetection()` no console do navegador (conforme a Seção 6) para simular a detecção de CEPs.

3.  **Observe o Movimento do Motor**: Ao simular a detecção de um CEP, o servidor Flask enviará o comando correspondente ao seu LEGO EV3. Você deverá observar o motor conectado à porta `A` do seu EV3 se movendo para a posição correta (esquerda, direita ou reto) de acordo com o "ponto de entrega" categorizado.

    *   **Ponto de Entrega 1 (Norte/Nordeste)**: Motor deve ir para a esquerda (-90 graus).
    *   **Ponto de Entrega 2 (Sul/Sudeste)**: Motor deve ir para a direita (90 graus).
    *   **Ponto de Entrega 3 (Centro-Oeste)**: Motor deve ir para a posição central (0 graus).

    Se o motor não se mover, verifique as mensagens de log no terminal do servidor Flask para identificar possíveis erros de comunicação com o EV3.




## 8. Solução de Problemas Comuns

*   **`ModuleNotFoundError` no Python**: Certifique-se de que você ativou o ambiente virtual e instalou as dependências usando `pip install -r requirements.txt`.
*   **Servidor Flask não inicia**: Verifique se não há erros de sintaxe no `main.py` ou `ev3_control.py`. Certifique-se de que a porta 5000 não está sendo usada por outro aplicativo.
*   **Frontend não se comunica com o Backend**: Verifique se o servidor Flask está rodando e se não há erros no console do navegador (F12). Erros de CORS podem ocorrer se o navegador estiver bloqueando a requisição (o Flask já está configurado para permitir CORS, mas extensões de navegador podem interferir).
*   **Câmera não aparece no scanner**: Verifique se você concedeu permissão de acesso à câmera no navegador. Tente reiniciar o navegador. Certifique-se de que nenhum outro aplicativo está usando a câmera.
*   **Motor do EV3 não se move**: Se estiver usando um EV3 real, verifique a conectividade de rede entre o computador e o EV3. Certifique-se de que o motor está conectado à porta correta (Porta A) e que o `ev3dev` está instalado e configurado corretamente no EV3.

## 9. Conclusão

Este guia deve fornecer todas as informações necessárias para você configurar e testar o projeto completo, desde o frontend até a simulação do controle do LEGO EV3. A integração com o EV3 real é um passo mais avançado que requer a configuração física do hardware, mas a base para a comunicação já está estabelecida.

Esperamos que este projeto seja útil e que você se divirta explorando a integração entre software e hardware!

---

**Autor:** Manus AI

**Referências:**

*   [Visual Studio Code](https://code.visualstudio.com/)
*   [Python Downloads](https://www.python.org/downloads/windows/)
*   [Git SCM](https://git-scm.com/download/win)
*   [Node.js Downloads](https://nodejs.org/en/download/)
*   [Flask Documentation](https://flask.palletsprojects.com/)
*   [ev3dev - Operating System for LEGO MINDSTORMS](https://www.ev3dev.org/)
*   [python-ev3dev Documentation](https://python-ev3dev.readthedocs.io/)
*   [ViaCEP API](https://viacep.com.br/)
*   [JSBarcode](https://lindell.github.io/jsbarcode/)
*   [QuaggaJS](https://serratus.github.io/quaggaJS/)


