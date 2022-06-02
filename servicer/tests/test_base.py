"""
Filename: test_base.py.

Copyright (c) 2021 - Present     Passport Fintech Inc.

All rights reserved.
"""

import random
import string
import unittest

# Imports the server definition
from package_server.server import Server  # pylint: disable=C0411


def generate_random_string(length):
    """
    Generate a random combination of lower and upper case characters.

    @param length: string length
    Returns: string
    """
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def generate_random_number_string(length):
    """
    Generate a random combination of numbers.

    @param length: string length
    Returns: string
    """
    return "".join(random.choice(string.digits) for i in range(length))


class PackageTestBase(unittest.TestCase):
    """Test the Server class implementation."""

    def setUp(self) -> None:
        """
        Set up  of test server. Initializes a mock service for all tests.

        @return: None
        """
        self.server = Server()
        self.server.graceful_shutdown_timer = 0
        self.server.serve()

    def tearDown(self) -> None:
        """
        Tear down of test server. Stops the mock service.

        @return: None
        """
        self.server.stop()
