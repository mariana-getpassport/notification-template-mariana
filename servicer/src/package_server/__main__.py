"""The main entry point into this package when run as a script."""

# For more details, see also
# https://docs.python.org/3/library/runpy.html
# https://docs.python.org/3/reference/import.html#special-considerations-for-main

import logging
import os
import sys
from concurrent import futures

import grpc
import package_grpc.v1.recommendations_pb2_grpc as rec_pb2_grpc
from opentelemetry.instrumentation.grpc import (  # type: ignore[import, attr-defined]
    GrpcInstrumentorClient,
    GrpcInstrumentorServer,
)
from opentelemetry.propagate import set_global_textmap  # type: ignore[import, attr-defined]
from opentelemetry.propagators.b3 import B3MultiFormat  # type: ignore[import, attr-defined]
from package_server import model
from utilities.log import init_logging

from . import recommendations

# Module logger.
_log = logging.getLogger(__name__)


def serve() -> None:
    """Create the grpc server."""
    # Setup B3 tracing headers propagation for grpc server and client
    set_global_textmap(B3MultiFormat())
    GrpcInstrumentorClient().instrument()
    GrpcInstrumentorServer().instrument()
    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=([]))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    rec_pb2_grpc.add_RecommendationsServicer_to_server(recommendations.RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    init_logging(disable_existing_loggers=False)
    _log.info("Initialized logging using config: %s", os.environ.get("PASSPORT_CONFIG"))
    if not model.get_tables():
        _log.info("Empty database. Creating tables and adding data.")
        model.create_tables()
        model.add_data()
    serve()
    sys.exit(os.EX_OK)
