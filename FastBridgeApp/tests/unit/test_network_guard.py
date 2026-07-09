"""Checks that the kill-switch in conftest.py actually works.

A unit test shouldn't be able to open a network socket, so it can't reach the production
database. If these tests fail, the isolation in conftest.py is broken and you can't trust
the rest of the suite to stay offline.
"""
import socket

import pytest
from pytest_socket import SocketBlockedError


def test_socket_creation_is_blocked():
    with pytest.raises(SocketBlockedError):
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def test_outbound_connection_is_blocked():
    with pytest.raises(SocketBlockedError):
        socket.create_connection(("example.com", 80), timeout=1)
