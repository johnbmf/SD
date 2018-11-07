import grpc
import time
from concurrent import futures

import aeropuerto_pb2
import aeropuerto_pb2_grpc

def cargar_combustible(avion):
    avion.combustible = avion.combustible_max
    print ("Combustible cargado exitosamente.\n")
    return

def ingresar_carga(avion):
    avion.carga = int(input("[Avion - " + avion.nombre + "]: Ingrese carga del avion: "))

class Avion:
    def __init__(self):
        print("Bienvenido al vuelo\n")
        self.nombre = str(input("Numero de avion: "))
        self.carga_max = int(input("[Avion - " + self.nombre + "]: Carga maxima en [Kg]: "))
        self.carga = 0
        self.combustible_max = int(input("[Avion - " + self.nombre + "]: Capacidad del tanque de combustible en [L]: "))
        self.combustible = self.combustible_max
        self.torre_control = str(input("[Avion - " + self.nombre + "]: Torre de control inicial: "))
        self.proveniente = "NOWHERE"
        self.destino = "NOWHERE"


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    avion = Avion()
    loop = True
    while (loop):
        channel = grpc.insecure_channel(avion.torre_control)  #localhost:50051
        stub = aeropuerto_pb2_grpc.AeropuertoStub(channel)
        #Creacion de la solicitud de aterrizaje
        mensaje = aeropuerto_pb2.AtRequest(nombre = avion.nombre, proveniente = avion.proveniente)
        resp = stub.Pedir_Aterrizaje(mensaje)
        print ("[Avion - " + avion.nombre + "]: Esperando pista de aterrizaje...\n")

        if (resp.respuesta == 0):
            print("Todas las pistas ocupadas. Avion predecesor es " + str(resp.pos_cola))
            while(resp.respuesta == 0):
                time.sleep(10)
                resp = stub.Pedir_Aterrizaje_Encolado(mensaje)

        if (resp.respuesta == 1):
            print("[Avion - " + avion.nombre + "]: Aterrizando en la pista " + str(resp.pista) + "...\n")


        loop_opciones = True
        while (loop_opciones):
            inp = int(input("Ingrese numero de tarea a ejecutar:\n1)Cargar combustible\n2)Ingresar cantidad de carga\n3)Solicitar despegue\n"))

            if (inp == 1):
                cargar_combustible(avion)
            elif (inp == 2):
                ingresar_carga(avion)
            elif (inp == 3):
                #crear mensaje
                avion.destino = str(input("Ingrese destino: "))
                mensaje = aeropuerto_pb2.DesRequest(nombre = avion.nombre, carga = avion.carga, carga_max = avion.carga_max,
                                                    combustible = avion.combustible, combustible_max = avion.combustible_max,
                                                    destino = avion.destino)
                resp = stub.Solicitar_despegue(mensaje)

                if (resp.respuesta == 0):
                    print("Carga maxima excedida o el combustible no esta completamente cargado. Verifique estos parametros.")
                if (resp.respuesta == 1):
                    print("Pista " + str(resp.pista) + " asiganda, altura de " + str(resp.altura) + "\n")
                    print("Despegando...\n")
                    avion.proveniente = resp.nombre_torre
                    avion.carga = 0
                    avion.combustible = 0
                    avion.torre_control = resp.torre_control
                    loop_opciones = False
                    input("Presione enter para solicitar aterrazaje en " + avion.destino)
if __name__ == '__main__':
    run()
