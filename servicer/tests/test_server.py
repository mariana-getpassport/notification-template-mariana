"""
Filename: test_server.py.

Copyright (c) 2021 - Present     Passport Fintech Inc.

All rights reserved.
"""

import os
from signal import SIGTERM

from .test_base import PackageTestBase


class TestServer(PackageTestBase):
    """Test the Server class implementation."""

    def test_service_signal_handling(self) -> None:
        """
        Test the service shutdown handler.

        @return: None
        """
        with self.assertRaises(SystemExit):
            pid = os.getpid()
            os.kill(pid, SIGTERM)
