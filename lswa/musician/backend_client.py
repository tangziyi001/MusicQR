import random
import grpc
import backend_pb2

def run_request(music_id, date):
    channel = grpc.insecure_channel('35.163.99.152:50050')
    stub = backend_pb2.BackendStub(channel)
    req = backend_pb2.MusicRequest(date=str(date), music_id=music_id)
    res = stub.GetDownloadRankDaily(req)
    return (res.date, res.count, res.rankNumber)

if __name__ == '__main__':
    run_request(1, '2016-12-04')
