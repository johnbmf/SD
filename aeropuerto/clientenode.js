/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
const readline = require('readline');
var PROTO_PATH = __dirname + '/../protos/aeropuerto.proto';
var grpc = require('grpc');
var protoLoader = require('@grpc/proto-loader');
var packageDefinition = protoLoader.loadSync(
  PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  });

  function msleep(n) {
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, n);
  }
  function sleep(n) {
    msleep(n*1000);
  }
var hello_proto = grpc.loadPackageDefinition(packageDefinition).aeropuerto;

var avion = {
  numero: '',
  carga: 0,
  combustible: 0,
  torre_inicial: ''
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
function solicitar_aterrizaje(nombre, proveniente) {
  var respuesta;
  var client = new hello_proto.Aeropuerto(avion.torre_inicial,
    grpc.credentials.createInsecure());
    var user;
    if (process.argv.length >= 3) {
      user = process.argv[2];
    } else {
      user = nombre;
    }
    client.Pedir_Aterrizaje({nombre: nombre, proveniente: proveniente}, function(err, response) {
      console.log('%s',nombre);
      respuesta = response.respuesta;
    });
      while (respuesta === 0) {
        console.log(`[Avion - ${nombre}]: Todas las pistas estan asignadas, el avion predecesor es PLACEHOLDER...`);
        sleep(10);
        solicitar_aterrizaje(nombre,proveniente);
      }
      if (response.respuesta === 1) {
        console.log(`[Avion - ${avion.numero}]: Está aterrizando en la pista: `, response.pista);
      }
}

function main() {
  solicitar_aterrizaje(avion.numero,avion.proveniente);
}
rl.question('Numero de avion: ', (answer) => {
  avion.numero = answer;
  rl.setPrompt(`[Avion - ${avion.numero}]: Carga maxima en [Kg]: `);
  rl.prompt();
  rl.on('line', (carga) => {
    avion.carga = carga;
    rl.question(`[Avion - ${avion.numero}]: Capacidad del tanque de combustible en [L]: `, (combustible) => {
      avion.combustible = combustible;
      rl.question(`[Avion - ${avion.numero}]: Torre de control inicial: `, (torre) => {
        avion.torre_inicial = torre;
        rl.close();
      });
    });
  });
});
rl.on('close', () => {
  main();
});
