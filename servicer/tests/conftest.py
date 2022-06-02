"""Configure the unit tests before they start running."""

# Copyright © 2021-2022 GetPassport. All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

import pytest
from package_server.server import create_server
from utilities.config import read_config


@pytest.fixture
def config():
    """Test fixture that reads configuration."""
    return read_config()


@pytest.fixture
def server():
    """Test fixture that creates and tears down a gRPC server for tests."""
    # Create and start the gRPC server for testing.
    rpc_server = create_server()
    rpc_server.start()

    # Return the server from this fixture to the unit test.
    yield rpc_server

    # Tear down the server and clean up after the test has run.
    rpc_server.stop(grace=0)
