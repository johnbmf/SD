import grpc
import time
from concurrent import futures

import aeropuerto_pb2
import aeropuerto_pb2_grpc

def crear_pistas(num_pistas_aterrizaje, num_pistas_despegue):
    pistas_aterrizaje = [None] * num_pistas_aterrizaje
    pistas_despegue = [None] * num_pistas_despegue
    return pistas_aterrizaje, pistas_despegue

def verificar_pista_disponible(lista_pistas):
    for i in range(len(lista_pistas)):
        if lista_pistas[i] == None:
            return i
    return -1;

class AeropuertoServicer(aeropuerto_pb2_grpc.AeropuertoServicer):

    def __init__(self):
        print("Bienvenido a la Torre de control\n")
        self.nombre = str(input("[Torre de control] Nombre del Aeropuerto: "))
        self.num_pistas_aterrizaje = int(input("[Torre de control - " + self.nombre + "] Cantidad de pistas de aterrizaje: "))
        self.num_pistas_despegue = int(input("[Torre de control - " + self.nombre + "] Cantidad de pistas de despegue: "))
        self.pA, self.pD = crear_pistas(self.num_pistas_aterrizaje, self.num_pistas_despegue)

        print (self.nombre)

    def Pedir_Aterrizaje(self, request, context):
        pista_disponible = verificar_pista_disponible(self.pA)

        if (pista_disponible != -1):
            print(request.nombre + " ha llegado al aeropuerto y se le asignara la pista " + str(pista_disponible) + "\n")
            self.pA[pista_disponible] = request.nombre
            #add info pantalla here

            #Respuesta
            respuesta = aeropuerto_pb2.AtReply(respuesta=1, pista=pista_disponible, altura=5, pos_cola=0)
            return(respuesta)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aeropuerto_pb2_grpc.add_AeropuertoServicer_to_server(AeropuertoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(50000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
