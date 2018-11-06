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
var torre = {
  nombre: ' ',
  paterrizaje: 0,
  pdespegue: 0,
};
var PROTO_PATH = __dirname + '/../protos/aeropuerto.proto';
const readline = require('readline');
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
var hello_proto = grpc.loadPackageDefinition(packageDefinition).aeropuerto;
/**
 * Implements the SayHello RPC method.
 */
function sayHello(call, callback) {
  console.log(call.request.name);
  callback(null, {message: ' esto viene desde el servidor: '});
}
/**
 * Starts an RPC server that receives requests for the Greeter service at the
 * sample server port
 */

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
rl.question('[Torre de Control] Nombre del Aeropuerto: ', (answer) => {
  torre.nombre = answer;
  rl.setPrompt(`[Torre de Control - ${torre.nombre}] Canitdad de pistas de aterrizaje: `);
  rl.prompt();
  rl.on('line',(pistas)=>{
    torre.paterrizaje = pistas;
    rl.question(`[Torre de Control - ${torre.nombre}] Canitdad de pistas de despegue: `, (despegue) =>{
      torre.pdespegue = despegue;
      rl.close();
    });
  });
});
function main() {
  var server = new grpc.Server();
  server.addService(hello_proto.Aeropuerto.service, {
    Pedir_Aterrizaje: sayHello
  });
  server.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure());
  server.start();
}

rl.on('close', ()=>{
  main();
  //console.log("%s %d %d", torre.nombre, torre.paterrizaje, torre.pdespegue);
});
