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
        TYPE (str | None): Type of the message (code identifier).
        writer (asyncio.StreamWriter): Writer object to send the message.
    """

    TYPE: str | None = None

    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self.writer = writer

    @property
    def type(self) -> str | None:
        """Return message type.

        Returns:
            str | none: Message type.
        """
        return self.TYPE

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
        data['type'] = self.TYPE
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

    TYPE = "log"

    def __init__(
        self,
        component: str,
        message: str,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.component = component
        self.message = message


class DroneCommandMessage(_BaseMessage):
    """Drone command message format.

    Attributes:
        target (str): Target drone to send the command.
        command (str): Command to execute.
        args (Any): Command arguments.

    Example:
        {
            'type': 'dcmd',
            'target': 'Drone-1',
            'command': 'moveto',
            'args': [10.0, 20.0]
        }
    """

    TYPE = "dcmd"

    def __init__(
        self,
        target: str,
        command: str,
        args: Any,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.target = target
        self.command = command
        self.args = args


class ServerCommandMessage(_BaseMessage):
    """Server command message format.

    Attributes:
        command (str): Command to execute.

    Example:
        {
            'type': 'scmd',
            'command': 'drones',
        }
    """

    TYPE = "scmd"

    def __init__(
        self,
        command: str,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.command = command


class ClientIdentificationMessage(_BaseMessage):
    """Client identification message format.

    Attributes:
        component (str): Component name.

    Example:
        {
            'type': 'cid',
            'component': 'Drone-1'
        }
    """

    TYPE = "cid"

    def __init__(
        self,
        component: str,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.component = component


class DroneStatusMessage(_BaseMessage):
    """Drone status message format.

    Attributes:
        component (str): Component that generated the status.
        location (dict): Location with longitude, latitude, and elevation.
        orientation (dict): Orientation with yaw, pitch, and roll.
        speed (float): Speed of the drone.
        autonomy (float): Autonomy of the drone.

    Example:
        {
            'type': 'dstat',
            'component': 'Drone-1',
            'location': {
                'longitude': 10.0,
                'latitude': 20.0,
                'elevation': 100.0
            },
            'orientation': {'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0},
            'speed': 5.0,
            'autonomy': 120.0
        }
    """

    TYPE = "dstat"

    def __init__(
        self,
        component: str,
        location: dict,
        orientation: dict,
        speed: float,
        autonomy: float,
        writer: asyncio.StreamWriter
    ) -> None:
        super().__init__(writer)
        self.component = component
        self.location = location
        self.orientation = orientation
        self.speed = speed
        self.autonomy = autonomy
