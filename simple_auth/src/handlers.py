import sys
sys.path.append("./proto")

from proto import auth_pb2_grpc

from src.grpc import Auth


def grpc_handlers(server):
    auth_pb2_grpc.add_AuthServicer_to_server(Auth.as_servicer(), server)
