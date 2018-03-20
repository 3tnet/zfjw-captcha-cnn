from concurrent import futures
import grpc
import data_pb2, data_pb2_grpc

_HOST = 'localhost'
_PORT = '8080'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = data_pb2_grpc.ImageToLabelStub(channel=conn)
    f = open('../1.png', 'rb')
    response = client.GetImageLabel(data_pb2.Image(imageBytes=f.read()))
    print("received: " + response.label)

if __name__ == '__main__':
    run()


