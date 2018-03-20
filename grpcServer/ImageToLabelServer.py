from concurrent import futures
import time

import grpc
import data_pb2, data_pb2_grpc
import sys
import os

sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..'))
import ImageToLabel

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = '[::]'
_PORT = '8080'

class ImageToLabelServer(data_pb2_grpc.ImageToLabelServicer):
  imageToLabel = ImageToLabel.ImageToLabel()
  def GetImageLabel(self, request, context):
      return data_pb2.Label(label = self.imageToLabel.getImageLabel(request.imageBytes))

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    data_pb2_grpc.add_ImageToLabelServicer_to_server(ImageToLabelServer(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()
