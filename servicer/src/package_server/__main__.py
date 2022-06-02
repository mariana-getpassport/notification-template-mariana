"""The main entry point into this package when run as a script."""

# For more details, see also
# https://docs.python.org/3/library/runpy.html
# https://docs.python.org/3/reference/import.html#special-considerations-for-main

import logging
import os
import sys
from concurrent import futures

import grpc
from opentelemetry.instrumentation.grpc import (  # type: ignore[import, attr-defined]
    GrpcInstrumentorClient,
    GrpcInstrumentorServer,
)
from opentelemetry.propagate import set_global_textmap  # type: ignore[import, attr-defined]
from opentelemetry.propagators.b3 import B3MultiFormat  # type: ignore[import, attr-defined]
from package_grpc.v1 import recommendations_pb2_grpc  # pylint: disable=C0411
from utilities.log import init_logging

from .recommendations import RecommendationService  # pylint: disable=E0402

# Module logger.
_log = logging.getLogger(__name__)


def serve() -> None:
    """Create the grpc server."""
    init_logging(disable_existing_loggers=False)
    _log.info("Initialized logging using config: %s", os.environ.get("PASSPORT_CONFIG"))
    # Setup B3 tracing headers propagation for grpc server and client
    set_global_textmap(B3MultiFormat())
    GrpcInstrumentorClient().instrument()
    GrpcInstrumentorServer().instrument()
    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=([]))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    sys.exit(os.EX_OK)
