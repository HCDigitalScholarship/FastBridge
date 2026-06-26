"""Network kill-switch for the unit tests.

The unit tests are pure logic and should never touch a database or the network. To make
that hard to get wrong, every test runs with sockets disabled. If something tries to open
a connection (for example, a stray import that reaches mongo_connection), it fails right
away with SocketBlockedError instead of quietly connecting to the production database.
"""
import pytest
from pytest_socket import disable_socket, enable_socket


@pytest.fixture(autouse=True)
def _no_network():
    disable_socket()
    yield
    enable_socket()
