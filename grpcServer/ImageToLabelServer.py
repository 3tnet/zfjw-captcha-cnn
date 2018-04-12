from concurrent import futures
import time
import grpc
import grpcServer.data_pb2 as data_pb2, grpcServer.data_pb2_grpc as data_pb2_grpc
import ImageToLabel

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = '[::]'
_PORT = '8080'


class ImageToLabelServer(data_pb2_grpc.ImageToLabelServicer):
    imageToLabel = ImageToLabel.ImageToLabel()

    def GetImageLabel(self, request, context):
        return data_pb2.Label(label=self.imageToLabel.getImageLabel(request.imageBytes))


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
