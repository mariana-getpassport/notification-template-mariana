"""
Filename: logger.py.

Copyright (c) 2021 - Present     Passport Fintech Inc.

All rights reserved.
"""
import logging

from grpc_interceptor import ServerInterceptor

logging.basicConfig(filename="/tmp/service.log", format="%(name)s - %(levelname)s - %(message)s")


class Logger(ServerInterceptor):  # pylint: disable=W0232
    """
    This logging implementation is temporary and will be replaced once the internal logging framework is complete.

    Defines a log file for the service when it is running in the container.
    """

    def intercept(self, method, request, context, method_name):
        """
        Intercept all calls and log any exceptions that are raised.

        @param method:
        @param request:
        @param context:
        @param method_name:
        @return:
        """
        try:
            return method(request, context)
        except Exception as exception:
            logging.exception("An exception has been raised.", exc_info=exception)
            raise
