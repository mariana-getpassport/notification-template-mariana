#!/bin/bash

folder="src/package_grpc"

if [[ "${VIRTUAL_ENV##*/}" = "venv" ]]; then
    search_path=${VIRTUAL_ENV}/..
else
    search_path=${VIRTUAL_ENV}
fi

#
# Check to see if the directory exists and if not, create it.
#

if [ ! -d $search_path/servicer_grpc/$folder ]; then
    # Control will enter here if $DIRECTORY exists.
    mkdir -p $search_path/servicer_grpc/$folder
fi

#
# Create the grpc files
#

python3 -m grpc_tools.protoc -I $search_path/protos/ \
    --python_out=$search_path/servicer_grpc/$folder \
    --grpc_python_out=$search_path/servicer_grpc/$folder \
    $search_path/protos/v*/*.proto

#
# Fix up the grpc files so that the imports are relative
#
#   NOTE: For versioned protos that have the folder layout
#         ./protos/v1/...
#         Use the search path:
#           $search_path/protos/v*/*.proto
#
for f1 in $search_path/protos/v*/*.proto; do
    target=$(basename $f1 .proto);
#    echo "filename: $f1 name: $target";
	find $search_path/servicer_grpc/$folder -type f \( -name "*_pb2_grpc.py" -o -name "*_pb2.py" \) -print0 | xargs -0 sed -i old -e 's/from v.* import '"$target"'_pb2/from . import '"$target"'_pb2/g'
	find $search_path/servicer_grpc/$folder -type f -name "*.pyold" -print0 | xargs -0 rm -rf
done
