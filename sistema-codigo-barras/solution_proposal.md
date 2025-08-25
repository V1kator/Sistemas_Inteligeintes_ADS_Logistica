# Proposta de Solução: Servidor Intermediário para Comunicação com LEGO EV3

## 1. Arquitetura da Solução

Para permitir que o site web se comunique com a esteira LEGO EV3, propõe-se a implementação de um servidor intermediário. Este servidor atuará como uma ponte, recebendo requisições do frontend (site web) e traduzindo-as em comandos que o LEGO EV3 pode entender e executar. A arquitetura será a seguinte:

```
[Frontend (Site Web)] <--- HTTP/HTTPS (Requisições REST) ---> [Servidor Intermediário (Python/Flask)] <--- Bluetooth/Wi-Fi/USB ---> [LEGO EV3]
```

-   **Frontend (Site Web)**: O site atual, desenvolvido em HTML, CSS e JavaScript, será responsável por:
    -   Escanear o código de barras e extrair o CEP.
    -   Categorizar o CEP em um "ponto de entrega" (1, 2 ou 3).
    -   Enviar o "ponto de entrega" para o servidor intermediário através de uma requisição HTTP (POST).

-   **Servidor Intermediário (Python/Flask)**: Um aplicativo web simples, construído com Python e o framework Flask, que será responsável por:
    -   Receber as requisições HTTP do frontend contendo o "ponto de entrega".
    -   Processar o "ponto de entrega" e determinar o comando apropriado para o LEGO EV3.
    -   Estabelecer comunicação com o LEGO EV3 (provavelmente via Bluetooth ou Wi-Fi, dependendo da configuração do EV3 e da biblioteca Python escolhida).
    -   Enviar o comando ao LEGO EV3 para controlar o motor do seletor.
    -   Retornar uma resposta ao frontend indicando o sucesso ou falha da operação.

-   **LEGO EV3**: O brick LEGO EV3, conectado à esteira e ao motor do seletor, será responsável por:
    -   Receber comandos do servidor intermediário.
    -   Executar a ação correspondente (mover o seletor para a esquerda, direita ou manter reto) usando o motor.

## 2. Detalhamento da Implementação da Comunicação

### 2.1. Comunicação Frontend para Servidor

O `scanner.js` no frontend será modificado para, após determinar o `pontoDeEntrega`, fazer uma requisição `fetch` (POST) para um endpoint específico no servidor intermediário. O corpo da requisição conterá o valor do `pontoDeEntrega`.

Exemplo de requisição (simplificado):

```javascript
fetch("http://endereco-do-servidor:porta/control_ev3", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ delivery_point: pontoDeEntrega })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Erro ao enviar comando para o EV3:", error));
```

### 2.2. Comunicação Servidor para LEGO EV3

No servidor Flask, será necessário:

1.  **Escolher uma Biblioteca de Comunicação**: A pesquisa inicial sugere `python-ev3dev` ou `ev3dev-lang-python` se o EV3 estiver rodando `ev3dev`. Se o EV3 estiver com o firmware padrão, outras opções como `pybricks` (que pode exigir um firmware customizado) ou comunicação via Bluetooth/USB de baixo nível podem ser exploradas. A escolha dependerá da facilidade de configuração e da robustez da comunicação.

2.  **Implementar a Lógica de Controle**: O servidor terá um endpoint (`/control_ev3`) que receberá o `delivery_point`. Com base nesse valor, o servidor usará a biblioteca escolhida para enviar comandos ao motor do LEGO EV3. Por exemplo:

    -   `delivery_point = 1`: Comando para mover o motor para a esquerda.
    -   `delivery_point = 2`: Comando para mover o motor para a direita.
    -   `delivery_point = 3`: Comando para manter o motor na posição neutra ou passar reto.

    Será crucial mapear os valores do `pontoDeEntrega` para ações específicas do motor (graus de rotação, direção, etc.).

### 2.3. Configuração do LEGO EV3

Para que o LEGO EV3 possa receber comandos do servidor, ele precisará estar configurado para comunicação de rede (Wi-Fi ou Bluetooth) e, idealmente, rodando um sistema operacional como `ev3dev` que permite a execução de scripts Python. Se o `ev3dev` for usado, o script Python no EV3 estaria ouvindo por comandos ou o servidor intermediário se conectaria diretamente a ele.

## 3. Próximos Passos

Com base nesta proposta, os próximos passos incluem:

-   Configurar o ambiente de desenvolvimento para o servidor Flask.
-   Instalar as bibliotecas necessárias para comunicação com o LEGO EV3 no servidor.
-   Desenvolver o código do servidor para receber e processar os comandos.
-   Implementar a lógica de controle do motor do EV3 no servidor.
-   Atualizar o frontend para enviar requisições ao servidor.
-   Realizar testes de integração completos para garantir que toda a cadeia de comunicação funcione conforme o esperado.

