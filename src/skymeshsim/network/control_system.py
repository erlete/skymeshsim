"""Control system module.

This module contains the ControlSystem class, which is responsible for sending
user commands to the server.

Author:
    Paulo Sanchez (@erlete)
"""


import asyncio

from .logger import Logger
from .messages import ClientIdentificationMessage, CommandMessage
from .network_component import _BaseNetworkComponent, _NetworkInputReader

COMMANDS = {
    "help": "Show this help message.",
    "moveto <longitude>, <latitude>": (
        "Move to the specified longitude and latitude coordinates."
    ),
    "exit": "Exit the ControlSystem."
}


class ControlSystem(_BaseNetworkComponent, _NetworkInputReader):
    """Sends user commands to the server."""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

        self._online = True
        self._logger = Logger(0, "[ControlSystem]")

    async def run(self) -> None:
        """Connect to the server and send user commands."""
        _, writer = await asyncio.open_connection(self.host, self.port)

        await ClientIdentificationMessage(
            component="ControlSystem",
            writer=writer
        ).send()

        self._logger.log("ControlSystem started.", 1)
        self._logger.log(
            "Type a command or 'help' to see a list of available commands.",
            1
        )

        # Main loop:
        try:
            while self._online:
                command = (await self.get_user_input()).strip().lower()

                # Internal operation commands:
                if command == "exit":
                    self._online = False
                    self._logger.log("Exiting ControlSystem.", 1)
                    continue

                elif command == "help":
                    max_command_length = max(len(cmd) for cmd in COMMANDS)
                    help_message = "Available commands:\n\n"
                    for command, description in COMMANDS.items():
                        help_message += (
                            f"  {command:<{max_command_length + 10}}"
                            + f" - {description}\n"
                        )

                    self._logger.log(help_message.strip(), 1)
                    continue

                # External operation commands:
                if command.lower().startswith("moveto"):
                    await CommandMessage(
                        command="moveto",
                        target=tuple(
                            map(float, command.split("moveto ")[1].split(","))
                        ),
                        writer=writer
                    ).send()
                else:
                    self._logger.log(
                        "Unknown command format. Type 'help' for a list of "
                        + "available commands.",
                        2
                    )

        except asyncio.CancelledError:
            self._logger.log("ControlSystem connection interrupted.", 2)

        finally:
            writer.close()
            await writer.wait_closed()
            self._logger.log("ControlSystem connection closed.", 1)


if __name__ == "__main__":
    # A single ControlSystem instance can be run per standalone application:
    control_system = ControlSystem(host="127.0.0.1", port=8888)
    asyncio.run(control_system.run())
