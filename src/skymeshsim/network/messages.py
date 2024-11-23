"""Message classes for communication between components.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

import asyncio
import json
from typing import Any


class _BaseMessage:
    """Base class for all messages. Handles JSON encoding/decoding.

    Attributes:
        writer (asyncio.StreamWriter): Writer object to send the message.
    """

    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self.writer = writer

    async def send(self) -> None:
        """Send the message to the server

        Raises:
            ConnectionError: If the connection is closed.
        """
        self.writer.write((self.to_json() + "\n").encode())
        await self.writer.drain()

    def to_json(self) -> str:
        """Encode the message to JSON format."""
        data = self.__dict__.copy()
        data.pop('writer', None)
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_data: str) -> _BaseMessage:
        """Decode the message from JSON format."""
        data = json.loads(json_data)
        return cls(**data)


class LogMessage(_BaseMessage):
    """Log message format.

    Attributes:
        component (str): Component that generated the log message.
        message (str): Log message

    Example:
        {
            'type': 'log',
            'component': 'Drone-1',
            'message': 'Received: {
                "type": "cmd",
                "command": "moveto",
                "target": [10.0, 20.0]
            }'
        }
    """

    def __init__(
        self,
        component: str,
        message: str,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.type = "log"
        self.component = component
        self.message = message


class DataMessage(_BaseMessage):
    """Data message format.

    Attributes:
        component (str): Component that generated the data.
        subtype (str): Data subtype.
        value (Any): Data value.

    Example:
        {
            'type': 'data',
            'component': 'Drone-1',
            'subtype': 'position',
            'value': {'x': 10.0, 'y': 20.0}
        }
    """

    def __init__(
        self,
        component: str,
        subtype: str,
        value: Any,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.type = "data"
        self.component = component
        self.subtype = subtype
        self.value = value


class CommandMessage(_BaseMessage):
    """Command message format.

    Attributes:
        command (str): Command to execute
        target (Any): Command target

    Example:
        {
            'type': 'cmd',
            'command': 'moveto',
            'target': (10.0, 20.0)
        }
    """

    def __init__(
        self,
        command: str,
        target: Any,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.type = "cmd"
        self.command = command
        self.target = target
