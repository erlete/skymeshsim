"""Network component base class module.

Author:
    Paulo Sanchez (@erlete)
"""


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
