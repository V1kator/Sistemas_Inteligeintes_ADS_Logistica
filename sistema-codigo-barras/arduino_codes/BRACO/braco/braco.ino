#include <Servo.h>

Servo sBase;
Servo sOmbro;
Servo sCotovelo;
Servo sGarra;

// Pinos dos servos
const int pinBase = 8;
const int pinOmbro = 9;
const int pinCotovelo = 10;
const int pinGarra = 11;

// Base
int baseNeutra = 90;
int baseDireita = 180;  // gira mais para direita
int baseEsquerda = 20;   // gira mais para esquerda

// Ombro/Cotovelo
int ombroAlto = 60;
int ombroBaixo = 160;        // braço abaixado para pegar
int cotoveloRecolhido = 90;  // menos recolhido, braço mais estendido ao subir
int cotoveloEstendido = 20;  // braço estendido para pegar/largar

// Garra
int garraAberta = 120;
int garraFechada = 0;        // máximo seguro

int stepDelay = 15; // suavidade do movimento

int ombroDescidaFinal = 140;       // menor descida que ombroBaixo
int cotoveloDescidaFinal = 80;     // menor extensão que cotoveloEstendido


void setup() {
  sBase.attach(pinBase);
  sOmbro.attach(pinOmbro);
  sCotovelo.attach(pinCotovelo);
  sGarra.attach(pinGarra);

  // Inicializa todos os servos suavemente na posição neutra
  moverSuave(sBase, baseNeutra);
  moverOmbroCotovelo(ombroAlto, cotoveloRecolhido);
  moverSuave(sGarra, garraAberta);

  delay(100);
}

void loop() {
  executarMovimentoCompleto();
  delay(100); // esperar antes de repetir
}

// Função principal: pegar e levar para direita
void executarMovimentoCompleto() {
  // 1. Posicao neutra (ombro, cotovelo, base, garra aberta)
  moverSuave(sBase, baseNeutra);
  moverOmbroCotovelo(ombroAlto, cotoveloRecolhido);
  moverSuave(sGarra, garraAberta);
  delay(500);

  // 2. Descer para pegar o objeto
  moverOmbroCotovelo(ombroBaixo, cotoveloEstendido);

  // 3. Fecha garra para segurar
  moverSuave(sGarra, garraFechada);
  delay(300);

  // 4. Sobe braço com objeto (cotovelo mais aberto, ombro alto)
  moverOmbroCotovelo(ombroAlto, cotoveloRecolhido);

  // 5. Gira base para a direita
  moverSuave(sBase, baseDireita);

// 6. Abaixa levemente para soltar objeto
moverOmbroCotovelo(ombroDescidaFinal, cotoveloDescidaFinal);

// 7. Abre garra para soltar
moverSuave(sGarra, garraAberta);
delay(300);


  // 8. Volta para posição neutra
  moverOmbroCotovelo(ombroAlto, cotoveloRecolhido);
  moverSuave(sBase, baseNeutra);
}

// Função para mover Ombro + Cotovelo juntos suavemente
void moverOmbroCotovelo(int targetOmbro, int targetCotovelo){
  int posOmbro = sOmbro.read();
  int posCotovelo = sCotovelo.read();

  while(posOmbro != targetOmbro || posCotovelo != targetCotovelo){
    if(posOmbro < targetOmbro) posOmbro++;
    else if(posOmbro > targetOmbro) posOmbro--;

    if(posCotovelo < targetCotovelo) posCotovelo++;
    else if(posCotovelo > targetCotovelo) posCotovelo--;

    sOmbro.write(posOmbro);
    sCotovelo.write(posCotovelo);
    delay(stepDelay);
  }
}

// Função para mover servo individual suavemente
void moverSuave(Servo &servo, int target){
  int pos = servo.read();
  if(pos < target){
    for(int p = pos; p <= target; p++){
      servo.write(p);
      delay(stepDelay);
    }
  } else {
    for(int p = pos; p >= target; p--){
      servo.write(p);
      delay(stepDelay);
    }
  }
}
