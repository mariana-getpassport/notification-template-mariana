"""
Filename: test_server.py.

Copyright (c) 2021 - Present     Passport Fintech Inc.

All rights reserved.
"""

import os
from signal import SIGTERM

import pytest


def test_service_signal_handling(server) -> None:  # pylint: disable=unused-argument
    """Test the service shutdown handler."""
    with pytest.raises(SystemExit):
        pid = os.getpid()
        os.kill(pid, SIGTERM)
