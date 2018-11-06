import grpc
import time
from concurrent import futures

import aeropuerto_pb2
import aeropuerto_pb2_grpc

class Avion:
    def __init__(self):
        print("Bienvenido al vuelo\n")
        self.nombre = str(input("Numero de avion: "))
        self.carga_max = int(input("[Avion - " + self.nombre + "]: Carga maxima en [Kg]: "))
        self.combustible_max = int(input("[Avion - " + self.nombre + "]: Capacidad del tanque de combustible en [L]: "))
        self.torre_control = str(input("[Avion - " + self.nombre + "]: Torre de control inicial: "))
        self.proveniente = "NOWHERE"


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    avion = Avion()
    channel = grpc.insecure_channel(avion.torre_control)  #localhost:50051
    stub = aeropuerto_pb2_grpc.AeropuertoStub(channel)

    #Creacion de la solicitud de aterrizaje
    mensaje = aeropuerto_pb2.AtRequest(nombre = avion.nombre, proveniente = avion.proveniente)
    resp = stub.Pedir_Aterrizaje(mensaje)
    print ("[Avion - " + avion.nombre + "]: Esperando pista de aterrizaje...\n")

    #caso de que si se puede aterrizar
    if (resp.respuesta == 1):
        print("[Avion - " + avion.nombre + "]: Aterrizando en la pista " + str(resp.pista) + "...\n")


if __name__ == '__main__':
    run()
