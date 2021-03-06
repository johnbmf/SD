# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import aeropuerto_pb2 as aeropuerto__pb2


class AeropuertoStub(object):
  """Servicio Aeropuerto

  Pedir aterrizaje: Solicitud de aterrizaje por parte del avion.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Pedir_Aterrizaje = channel.unary_unary(
        '/aeropuerto.Aeropuerto/Pedir_Aterrizaje',
        request_serializer=aeropuerto__pb2.AtRequest.SerializeToString,
        response_deserializer=aeropuerto__pb2.AtReply.FromString,
        )
    self.Pedir_Aterrizaje_Encolado = channel.unary_unary(
        '/aeropuerto.Aeropuerto/Pedir_Aterrizaje_Encolado',
        request_serializer=aeropuerto__pb2.AtRequest.SerializeToString,
        response_deserializer=aeropuerto__pb2.AtReply.FromString,
        )
    self.Solicitar_despegue = channel.unary_unary(
        '/aeropuerto.Aeropuerto/Solicitar_despegue',
        request_serializer=aeropuerto__pb2.DesRequest.SerializeToString,
        response_deserializer=aeropuerto__pb2.DesReply.FromString,
        )


class AeropuertoServicer(object):
  """Servicio Aeropuerto

  Pedir aterrizaje: Solicitud de aterrizaje por parte del avion.
  """

  def Pedir_Aterrizaje(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Pedir_Aterrizaje_Encolado(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Solicitar_despegue(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AeropuertoServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Pedir_Aterrizaje': grpc.unary_unary_rpc_method_handler(
          servicer.Pedir_Aterrizaje,
          request_deserializer=aeropuerto__pb2.AtRequest.FromString,
          response_serializer=aeropuerto__pb2.AtReply.SerializeToString,
      ),
      'Pedir_Aterrizaje_Encolado': grpc.unary_unary_rpc_method_handler(
          servicer.Pedir_Aterrizaje_Encolado,
          request_deserializer=aeropuerto__pb2.AtRequest.FromString,
          response_serializer=aeropuerto__pb2.AtReply.SerializeToString,
      ),
      'Solicitar_despegue': grpc.unary_unary_rpc_method_handler(
          servicer.Solicitar_despegue,
          request_deserializer=aeropuerto__pb2.DesRequest.FromString,
          response_serializer=aeropuerto__pb2.DesReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'aeropuerto.Aeropuerto', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
