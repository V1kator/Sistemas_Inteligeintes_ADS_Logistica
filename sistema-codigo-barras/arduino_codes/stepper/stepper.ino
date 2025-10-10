#include <Stepper.h>
//2062 eh o valor bom
const int stepsPerRevolution = 2062;  
Stepper myStepper(stepsPerRevolution, 2, 4, 3, 5);  // ordem corrigida

void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(12);
  Serial.println("Arduino pronto! Digite DIREITA ou ESQUERDA.");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando.equalsIgnoreCase("DIREITA")) {
      Serial.println("Girando 360° para DIREITA...");
      myStepper.step(stepsPerRevolution);
      Serial.println("Concluído.");
    } 
    else if (comando.equalsIgnoreCase("ESQUERDA")) {
      Serial.println("Girando 360° para ESQUERDA...");
      myStepper.step(-stepsPerRevolution);
      Serial.println("Concluído.");
    } 
    else {
      Serial.println("Comando invalido! Use DIREITA ou ESQUERDA.");
    }
  }
}
