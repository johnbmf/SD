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
  msleep(n * 1000);
}
var hello_proto = grpc.loadPackageDefinition(packageDefinition).aeropuerto;

var avion = {
  nombre: '',
  carga_max: 20,
  carga: 0,
  combustible_max: 50,
  proveniente: '',
  destino: '',
  combustible: 0,
  torre_control: ''
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function cargar_combustible(av, rl2) {
  av.combustible = av.combustible_max;
  console.log("Combustible cargado exitosamente.\n");
  Consultar_opciones(rl2);
}

function ingresar_carga(av, valor, rl2) {
  av.carga = valor;
  Consultar_opciones(rl2);
}

function Consultar_opciones(rl2) {
  var valor;
  rl2.question("Ingrese numero de tarea a ejecutar:\n1)Cargar combustible\n2)Ingresar cantidad de carga\n3)Solicitar despegue\n", (answer) => {
    valor = answer;
    if (valor == 1) {
      cargar_combustible(avion, rl2);
      return true;
    }
    if (valor == 2) {
      rl2.question(`[Avion ${avion.nombre}]: Ingrese carga del avion`, (answer) => {
        ingresar_carga(avion, answer, rl2);
        return true;
      });
    } else {
      console.log("entre al else \n");
      rl2.setPrompt(`Ingrese destino: `);
      rl2.prompt();
      return false;
    }
  });
}

function solicitar_aterrizaje(nombre, proveniente, torre_control, loop_opciones,callback) {
  var f;
  var rl2 = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  console.log("1\n");
  var loop = loop_opciones;
  var respuesta;
  //while (loop) {
  var client = new hello_proto.Aeropuerto(torre_control,
    grpc.credentials.createInsecure());
  var user;
  if (process.argv.length >= 3) {
    user = process.argv[2];
  } else {
    user = nombre;
  }
  console.log("1,1\n");
  client.Pedir_Aterrizaje({
    nombre: nombre,
    proveniente: proveniente
  }, function(err, response) {
    console.log('%s', nombre);
    respuesta = response.respuesta;
    console.log("1.2\n");
    if (respuesta === 0) {
      console.log("2\n");
      console.log(`[Avion - ${nombre}]: Todas las pistas estan asignadas, el avion predecesor es ${response.pos_cola}...`);
      while (respuesta === 0) {
        sleep(10);
        client.Pedir_Aterrizaje_Encolado({
          nombre: nombre,
          proveniente: proveniente
        }, (err, response) => {
          respuesta = response.respuesta;
        });
      }

    }
    console.log("1,2\n");
    if (respuesta === 1) {
      console.log("3\n");
      console.log(`[Avion - ${avion.nombre}]: Está aterrizando en la pista: `, response.pista);
      loop = true;
    }

    //while (loop_opciones) {
    //rl2.pause();
    if (loop) {

      Consultar_opciones(rl2);

      rl2.on('line', (d) => {
        avion.destino = d;
        client.Solicitar_despegue({
          nombre: avion.nombre,
          carga: avion.carga,
          carga_max: avion.carga_max,
          combustible: avion.combustible,
          combustible_max: avion.combustible_max,
          destino: avion.destino
        }, (err, response) => {
          if (response.respuesta === 0) {
            console.log(avion);
            console.log("Carga maxima excedida o el combustible no esta completamente cargado. Verifique estos parametros.");
            Consultar_opciones(rl2);
          }
          if (response.respuesta === 1) {
            console.log(`Pista ${response.pista} asignada, altura de ${response.altura} \n`);
            console.log("Despegando... \n");
            avion.proveniente = response.nombre_torre;
            avion.carga = 0;
            avion.combustible = 0;
            avion.torre_control = response.torre_control;
            loop_opciones = false;
            rl2.question(`Presione enter para solicitar aterrizaje en ${avion.destino}`, (answer) => {
              sleep(10);
              console.log(avion.torre_control);
              callback(avion.nombre, avion.proveniente, avion.torre_control, false);
              //solicitar_aterrizaje(avion.nombre, avion.proveniente, avion.torre_control, false);
            });
          }

        });
      });
    }

    //}
  });
  //}
}


function main() {

  solicitar_aterrizaje(avion.nombre, avion.proveniente, avion.torre_control, true);
}
rl.question('Numero de avion: ', (answer) => {
  avion.nombre = answer;
  rl.setPrompt(`[Avion - ${avion.nombre}]: Carga maxima en [Kg]: `);
  rl.prompt();
  rl.on('line', (carga) => {
    avion.carga = carga;
    rl.question(`[Avion - ${avion.nombre}]: Capacidad del tanque de combustible en [L]: `, (combustible) => {
      avion.combustible = combustible;
      rl.question(`[Avion - ${avion.nombre}]: Torre de control inicial: `, (torre) => {
        avion.torre_control = torre;
        rl.close();
      });
    });
  });
});
rl.on('close', () => {
  main();
});
