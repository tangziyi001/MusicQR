#!/bin/bash
python -m grpc.tools.protoc -I./protos --python_out=./python --grpc_python_out=./python ./protos/backend.proto
