const express = require("express");
const { SerialPort } = require("serialport");
const { ReadlineParser } = require("@serialport/parser-readline");

const app = express();
const port = 3000;

// ajuste "COM3" ou "/dev/ttyACM0" conforme seu SO
const arduino = new SerialPort({ path: "COM8", baudRate: 9600 });
const parser = arduino.pipe(new ReadlineParser({ delimiter: "\n" }));

parser.on("data", (line) => {
  console.log("Arduino:", line);
});

app.get("/direita", (req, res) => {
  arduino.write("DIREITA\n");
  res.send("Comando enviado: DIREITA");
});

app.get("/esquerda", (req, res) => {
  arduino.write("ESQUERDA\n");
  res.send("Comando enviado: ESQUERDA");
});

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
