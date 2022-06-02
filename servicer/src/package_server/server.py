"""
Filename: server.py.

Copyright (c) 2021 - Present     Passport Fintech Inc.

All rights reserved.
"""
from concurrent import futures
from signal import SIGTERM, signal

import grpc
from package_grpc.v1 import recommendations_pb2_grpc  # pylint: disable=C0411

from . import logger
from .recommendations import RecommendationService  # pylint: disable=E0402


class Server:
    """Defines the service server definition."""

    def __init__(self):
        """Initialize the grpc server and set the interceptors for logging."""
        self.interceptors = [logger.Logger()]
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=self.interceptors)
        self.graceful_shutdown_timer = 15
        self.host = "[::]"
        self.port = 50051

    def serve(self) -> None:
        """
        Define the Route Handlers the server will handle.

        @return: None
        """

        def handle_sigterm(*_):
            all_rpcs_done_event = self.server.stop(self.graceful_shutdown_timer)
            all_rpcs_done_event.wait(self.graceful_shutdown_timer)
            raise SystemExit

        # Add API handlers here.
        recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), self.server)

        self.server.add_insecure_port(f"{self.host}:{self.port}")
        self.server.start()

        signal(SIGTERM, handle_sigterm)

        self.server.wait_for_termination(timeout=self.graceful_shutdown_timer)

    def stop(self) -> None:
        """
        Handle the server shutdown.

        @return: None
        """
        self.server.stop(grace=self.graceful_shutdown_timer)
