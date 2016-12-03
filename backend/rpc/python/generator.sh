#!/bin/bash
python -m grpc.tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/backend.proto
