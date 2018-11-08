import grpc
import time
from concurrent import futures

import aeropuerto_pb2
import aeropuerto_pb2_grpc
import collections

def abrir_puertos(aer_serv, server):
    if (aer_serv.nombre in ["Santiago", 'santiago', 'SANTIAGO']):
        server.add_insecure_port('[::]:50051')
        server.add_insecure_port('[::]:50052')
    elif (aer_serv.nombre in ["Antofagasta", 'antofagasta', 'ANTOFAGASTA']):
        server.add_insecure_port('[::]:50061')
        server.add_insecure_port('[::]:50062')
    elif (aer_serv.nombre in ["Lima", 'lima', 'LIMA']):
        server.add_insecure_port('[::]:50071')
        server.add_insecure_port('[::]:50072')
    return


def crear_pistas(num_pistas_aterrizaje, num_pistas_despegue):
    pistas_aterrizaje = [None] * num_pistas_aterrizaje
    pistas_despegue = [None] * num_pistas_despegue
    return pistas_aterrizaje, pistas_despegue

def verificar_pista_disponible(lista_pistas):
    for i in range(len(lista_pistas)):
        if lista_pistas[i] == None:
            return i
    return -1;

def check_destino(destino):
    if (destino in ["Santiago", 'santiago', 'SANTIAGO']):
        return "localhost:50051"
    elif (destino in ["Antofagasta", 'antofagasta', 'ANTOFAGASTA']):
        return "localhost:50061"
    elif (destino in ["Lima", 'lima', 'LIMA']):
        return "localhost:50071"

class AeropuertoServicer(aeropuerto_pb2_grpc.AeropuertoServicer):

    def __init__(self):
        print("Bienvenido a la Torre de control\n")
        self.nombre = str(input("[Torre de control] Nombre del Aeropuerto: "))
        self.num_pistas_aterrizaje = int(input("[Torre de control - " + self.nombre + "] Cantidad de pistas de aterrizaje: "))
        self.num_pistas_despegue = int(input("[Torre de control - " + self.nombre + "] Cantidad de pistas de despegue: "))
        self.pA, self.pD = crear_pistas(self.num_pistas_aterrizaje, self.num_pistas_despegue)
        self.cola = collections.deque([])

        print (self.nombre)

    def Pedir_Aterrizaje(self, request, context):
        pista_disponible = verificar_pista_disponible(self.pA)

        if (pista_disponible != -1):
            print(request.nombre + " ha llegado al aeropuerto y se le asignara la pista " + str(pista_disponible + 1) + "\n")
            self.pA[pista_disponible] = request.nombre
            #add info pantalla here

            #Respuesta
            respuesta = aeropuerto_pb2.AtReply(respuesta=1, pista=pista_disponible, altura=5, pos_cola="")
            return(respuesta)
        else:
            print("Todas las pistas ocupadas, encolando avion \n")
            if len(self.cola) == 0:
                predecesor = "ninguno (primero en la cola)"
            else:
                predecesor = self.cola[-1]
            self.cola.append(request.nombre)
            respuesta = aeropuerto_pb2.AtReply(respuesta = 0, pista = 0, altura = 5*len(self.cola), pos_cola = predecesor)
            return(respuesta)

    def Pedir_Aterrizaje_Encolado(self, request, context):
        if (self.cola[0] == request.nombre):
            pista_disponible = verificar_pista_disponible(self.pA)

            if (pista_disponible == -1):
                respuesta = aeropuerto_pb2.AtReply(respuesta = 0, pista = 0, altura = 5, pos_cola = "")
                return (respuesta)

            else:
                respuesta = aeropuerto_pb2.AtReply(respuesta=1, pista=pista_disponible, altura=5, pos_cola="")
                self.cola.popleft()
                return (respuesta)

        else:
            respuesta = aeropuerto_pb2.AtReply(respuesta = 0, pista = 0, altura = 5, pos_cola = "")
            return (respuesta)

    def Solicitar_despegue(self, request, context):
        print("[Torre de control - " + self.nombre + "] " + request.nombre + " solicita un despegue.\n")
        #Verifica combustible lleno
        if (request.combustible < request.combustible_max):
            print("[Torre de control - " + self.nombre + "] " + request.nombre + " no cumple con el combustible solicitado\n")
            respuesta = aeropuerto_pb2.DesReply(respuesta = 0, pista = 0, altura = 0, nombre_torre = self.nombre,
                                                torre_control = "")
        elif (request.carga > request.carga_max):
            print("[Torre de control - " + self.nombre + "] " + request.nombre + " no cumple con carga maxima.\n")
            respuesta = aeropuerto_pb2.DesReply(respuesta = 0, pista = 0, altura = 0, nombre_torre = self.nombre,
                                                torre_control = "")
        else:
            puerto_destino = check_destino(request.destino)
            respuesta = aeropuerto_pb2.DesReply(respuesta = 1, pista = 1, altura = 10, nombre_torre = self.nombre,
                                                torre_control = puerto_destino)
            self.pA[self.pA.index(request.nombre)] = None
            print("[Torre de control - " + self.nombre + "] " + request.nombre + " despego del aeropuerto.\n")
        return respuesta

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aer_serv = AeropuertoServicer()
    aeropuerto_pb2_grpc.add_AeropuertoServicer_to_server(aer_serv, server)
    abrir_puertos(aer_serv, server)
    server.start()
    try:
        while True:
            time.sleep(50000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
