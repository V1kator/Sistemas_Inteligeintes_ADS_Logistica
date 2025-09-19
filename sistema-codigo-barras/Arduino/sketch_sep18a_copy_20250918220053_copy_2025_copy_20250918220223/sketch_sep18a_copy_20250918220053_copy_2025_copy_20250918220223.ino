#include <Stepper.h>

const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(60);  // Ajuste a velocidade
  Serial.println("Sistema iniciado. Aguardando ponto de entrega...");
}

void loop() {
  if (Serial.available() > 0) {
    int ponto = Serial.parseInt();
    Serial.print("Recebi ponto de entrega: ");
    Serial.println(ponto);

    if (ponto == 1) {
      Serial.println("Movendo motor para ESQUERDA");
      myStepper.step(-stepsPerRevolution);
    } else if (ponto == 2) {
      Serial.println("Movendo motor para DIREITA");
      myStepper.step(stepsPerRevolution);
    } else if (ponto == 3) {
      Serial.println("Movendo motor RETO");
      myStepper.step(stepsPerRevolution / 2);
    } else {
      Serial.println("Valor inválido recebido.");
    }
  }
}
