#include <Servo.h>
#include <Stepper.h>

// ====== SERVOS ======
Servo sBase;
Servo sOmbro;
Servo sCotovelo;
Servo sGarra;

// Pinos dos servos
const int pinBase = 8;
const int pinOmbro = 9; // o ombro eh o da esquerda
const int pinCotovelo = 10; //o cotovelo eh o da direita (ponto de referencia olhar a garra de frente)
const int pinGarra = 11;  

// Base
int baseNeutra = 90;
int baseDireita = 180;  
int baseEsquerda = 0;  

// Ombro/Cotovelo
int ombroAlto = 60;
int ombroBaixo = 160;        
int cotoveloRecolhido = 90;  
int cotoveloEstendido = 0;  

// Garra
int garraAberta = 120;
int garraFechada = 0;        

int stepDelay = 15; 

int ombroDescidaFinal = 140;      
int cotoveloDescidaFinal = 80;    

// ====== STEPPER ======
const int stepsPerRevolution = 2056;  
Stepper myStepper(stepsPerRevolution, 2, 4, 3, 5);  // ordem corrigida

// ====== VARIÁVEIS DE MOVIMENTO DO BRACO ======
struct ServoMove {
  Servo* servo;
  int target;
};
ServoMove movimento[4]; // Base, Ombro, Cotovelo, Garra
bool BracoAtivo = false;
int passo = 1;
unsigned long ultimoStep = 0;

// Sequência do Braco
enum EstadoBraco {
  NEUTRO,
  DESCER,
  FECHAR_GARRA,
  SUBIR,
  GIRAR_BASE,
  ABAIXAR_LEVEMENTE,
  ABRIR_GARRA,
  VOLTAR_NEUTRO
};
EstadoBraco estadoAtual = NEUTRO;

// ====== SETUP ======
void setup() {
  sBase.attach(pinBase);
  sOmbro.attach(pinOmbro);
  sCotovelo.attach(pinCotovelo);
  sGarra.attach(pinGarra);

  sBase.write(baseNeutra);
  sOmbro.write(ombroAlto);
  sCotovelo.write(cotoveloRecolhido);
  sGarra.write(garraAberta);

  Serial.begin(9600);
  Serial.setTimeout(50); // resposta imediata
  myStepper.setSpeed(12);
  Serial.println("Arduino pronto!");
  Serial.println("Comandos para o Stepper: DIREITA / ESQUERDA");
}

// ====== LOOP ======
void loop() {
  // Processa comandos Serial
  processSerial();

  // Executa movimento do Braco
  executarMovimentoCompletoNaoBloqueante();
}

// ====== FUNÇÕES SERIAL ======
void processSerial() {
  while (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando.equalsIgnoreCase("DIREITA")) {
      Serial.println("Girando 360° para DIREITA...");
      delay(3000);
      myStepper.step(stepsPerRevolution);
      Serial.println("Concluído.");
    } 
    else if (comando.equalsIgnoreCase("ESQUERDA")) {
      Serial.println("Girando 360° para ESQUERDA...");
      delay(3000);
      myStepper.step(-stepsPerRevolution);
      Serial.println("Concluído.");
    } 
    else {
      Serial.println("Comando inválido! Use DIREITA ou ESQUERDA.");
    }
  }
}

// ====== FUNÇÕES DO BRACO ======
void executarMovimentoCompletoNaoBloqueante() {
  if (millis() - ultimoStep < stepDelay) return;
  ultimoStep = millis();

  switch (estadoAtual) {
    case NEUTRO:
      setMovimento(baseNeutra, ombroAlto, cotoveloRecolhido, garraAberta);
      estadoAtual = DESCER;
      break;

    case DESCER:
      if (moverServosPara(ombroBaixo, cotoveloEstendido)) {
        estadoAtual = FECHAR_GARRA;
      }
      break;

    case FECHAR_GARRA:
      if (moverServosParaGarra(garraFechada)) {
        estadoAtual = SUBIR;
      }
      break;

    case SUBIR:
      if (moverServosPara(ombroAlto, cotoveloRecolhido)) {
        estadoAtual = GIRAR_BASE;
      }
      break;

    case GIRAR_BASE:
      if (moverServoBase(baseDireita)) {
        estadoAtual = ABAIXAR_LEVEMENTE;
      }
      break;

    case ABAIXAR_LEVEMENTE:
      if (moverServosPara(ombroDescidaFinal, cotoveloDescidaFinal)) {
        estadoAtual = ABRIR_GARRA;
      }
      break;

    case ABRIR_GARRA:
      if (moverServosParaGarra(garraAberta)) {
        estadoAtual = VOLTAR_NEUTRO;
      }
      break;

    case VOLTAR_NEUTRO:
      if (moverServosPara(ombroAlto, cotoveloRecolhido) && moverServoBase(baseNeutra)) {
        estadoAtual = NEUTRO; // reinicia o ciclo
      }
      break;
  }
}

// Inicializa alvo do movimento
void setMovimento(int baseT, int ombroT, int cotoveloT, int garraT) {
  movimento[0] = {&sBase, baseT};
  movimento[1] = {&sOmbro, ombroT};
  movimento[2] = {&sCotovelo, cotoveloT};
  movimento[3] = {&sGarra, garraT};
  BracoAtivo = true;
}

// Move base sozinho
bool moverServoBase(int alvo) {
  int posAtual = sBase.read();
  if (posAtual < alvo) {
    sBase.write(posAtual + passo);
    return false;
  } else if (posAtual > alvo) {
    sBase.write(posAtual - passo);
    return false;
  }
  return true;
}

// Move ombro + cotovelo
bool moverServosPara(int alvoOmbro, int alvoCotovelo) {
  bool pronto = true;

  int posOmbro = sOmbro.read();
  int posCotovelo = sCotovelo.read();

  if (posOmbro < alvoOmbro) { sOmbro.write(posOmbro + passo); pronto = false; }
  else if (posOmbro > alvoOmbro) { sOmbro.write(posOmbro - passo); pronto = false; }

  if (posCotovelo < alvoCotovelo) { sCotovelo.write(posCotovelo + passo); pronto = false; }
  else if (posCotovelo > alvoCotovelo) { sCotovelo.write(posCotovelo - passo); pronto = false; }

  return pronto;
}

// Move apenas garra
bool moverServosParaGarra(int alvoGarra) {
  int posAtual = sGarra.read();
  if (posAtual < alvoGarra) { sGarra.write(posAtual + passo); return false; }
  else if (posAtual > alvoGarra) { sGarra.write(posAtual - passo); return false; }
  return true;
}
