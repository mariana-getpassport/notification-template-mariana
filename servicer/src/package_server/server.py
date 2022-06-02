"""
Filename: server.py.

Copyright (c) 2021 - Present     Passport Fintech Inc.

All rights reserved.
"""
import concurrent.futures
import logging
import signal

import grpc
from package_grpc.v1 import recommendations_pb2_grpc  # pylint: disable=C0411
from utilities.config import read_config

from . import logger
from .recommendations import RecommendationService  # pylint: disable=E0402

# Module logger.
_log = logging.getLogger(__name__)


def create_server():
    """Create a gRPC server instance and return it."""
    # TODO Consider moving this into the utilities.rpc sub-package
    # TODO If the server spawns multiple processes then we need to hook into their
    # creation and set up logging (and signal handling) for those processes.

    # Read the global app configuration file and get the gRPC values.
    config = read_config()
    max_workers = config.getint("grpc", "server.max_workers")
    graceful_shutdown_timer = config.getint("grpc", "server.graceful_shutdown_timer")
    host = config.get("grpc", "server.host")
    port = config.getint("grpc", "server.port")

    # Create the gRPC server.
    interceptors = [logger.Logger()]
    rpc_server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=max_workers), interceptors=interceptors)
    rpc_server.add_insecure_port(f"{host}:{port}")

    # Register a signal handler for this process.
    def handle_signal(signum, frame):  # pylint: disable=unused-argument
        _log.info("Received signal %s, stopping server", signum)
        all_rpcs_done_event = rpc_server.stop(grace=graceful_shutdown_timer)
        all_rpcs_done_event.wait(graceful_shutdown_timer)
        raise SystemExit

    _ = signal.signal(signal.SIGTERM, handle_signal)
    _ = signal.signal(signal.SIGINT, handle_signal)  # Ctrl-C

    # Add API handlers here.
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), rpc_server)

    # Done.
    return rpc_server
