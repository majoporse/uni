""" The PV080 server (https://pv080.fi.muni.cz/) provides a functionality to
exchange `messages` between students. The ``type`` of the content of the message
is :py:class:`bytes`. To send a message to a particular UČO use the function
:py:mod:`send_message <pv080_crypto.messages.send_message>` and to receive a
message use the :py:mod:`recv_message <pv080_crypto.messages.recv_message>`
function.

Each message comes from a sender UČO and is sent to another UČO (the sender and
the receiver can be the same person). For every pair of UČO only **the last**
message is recorded.
"""
from typing import Mapping, Union
from binascii import hexlify, unhexlify

import requests

from pv080_crypto.config import SERVER_MESSAGE_PATH


def send_message(uco_from: int, uco_to: int, content: bytes) -> str:
    """
    Sends the ``content`` to https://pv080.fi.muni.cz/msg server, where it is readable by
    anyone on the internet.

    :param uco_from: Is the UČO of the sender.
    :param uco_to: Is the UČO of the receiver.
    :param content: Is the message encoded in bytes.

    :returns: The status message of the result of this API call to the server.

    Example:

    >>> send_message(uco_from=408788, uco_to=408788, content=b"message")
    'overwritten'
    """
    data = {
        "from": uco_from,
        "to": uco_to,
        "content": hexlify(content).decode(),
    }

    resp = requests.post(
        SERVER_MESSAGE_PATH,
        json=data,
    )

    return resp.json()["status"]


def recv_message(uco: int) -> Mapping[str, Union[int, bytes]]:
    """
    Receive the messages that have been sent to ``uco``.

    :param uco: Is the UČO of the addressee/receiver.

    :returns: A dictionary where the keys are UČOs of the senders and values are their messages.

    Example:

    >>> send_message(uco_from=408788, uco_to=408788, content=b"message")
    'overwritten'
    >>> messages = recv_message(uco=408788)
    >>> message_from_408788 = messages[408788]
    >>> assert message_from_408788 == b"message"
    """
    resp = requests.get(
        SERVER_MESSAGE_PATH,
        params={"uco": uco},
    )

    messages = {}
    if resp.status_code == 200:
        data = resp.json()
        for msg in data:
            # NOTE: at the moment there is only a single message per user
            # so no key collisions - apart from no auth/DoS that was there already
            messages[msg["from"]] = unhexlify(msg["content"])

    return messages
