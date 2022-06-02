"""The main entry point into this package when run as a script."""

# For more details, see also
# https://docs.python.org/3/library/runpy.html
# https://docs.python.org/3/reference/import.html#special-considerations-for-main

import os
import sys
from concurrent import futures

import grpc
from package_grpc.v1 import recommendations_pb2_grpc  # pylint: disable=C0411

from .recommendations import RecommendationService  # pylint: disable=E0402


def serve() -> None:
    """Create the grpc server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    sys.exit(os.EX_OK)
