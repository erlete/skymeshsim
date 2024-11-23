"""Network component base class module.

Author:
    Paulo Sanchez (@erlete)
"""


import asyncio


class _BaseNetworkComponent:
    """Network component base class.

    Attributes:
        host (str): Host address.
        port (int): Port number.
    """

    def __init__(self, host: str, port: int) -> None:
        """Initialize a NetworkComponent instance."""
        self.host = host
        self.port = port


class _NetworkInputReader:
    """Network input reader mixin class."""

    async def get_user_input(self) -> str:
        """Asynchronously get user input."""
        print("> ", end="", flush=True)
        return await asyncio.get_event_loop().run_in_executor(None, input)
