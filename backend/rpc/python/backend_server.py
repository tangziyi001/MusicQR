"""The Python implementation of the GRPC backend server."""

from concurrent import futures
import time
import grpc
import backend_pb2
from query_sql import retrieve_rank 

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Backend(backend_pb2.BackendServicer):
    def GetDownloadRankDaily(self, request, context):
        (music_id, count, rank, date) = retrieve_rank(request.music_id, request.date)
        return backend_pb2.RankInfo(date=str(date), count=count, rankNumber=rank)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2.add_BackendServicer_to_server(Backend(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

