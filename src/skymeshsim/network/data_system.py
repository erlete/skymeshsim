import asyncio
import json

from .network_component import _BaseNetworkComponent


class DataSystem(_BaseNetworkComponent):
    """Logs messages received from the server."""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    async def run(self) -> None:
        """Connect to the server and log messages."""
        reader, writer = await asyncio.open_connection(self.host, self.port)
        writer.write(b"DataSystem\n")
        await writer.drain()

        try:
            while True:
                message = await reader.readline()
                if not message:
                    break
                try:
                    # Decode and parse the JSON message
                    decoded_message = json.loads(message.decode().strip())
                    print(f"Log: {decoded_message}")
                except json.JSONDecodeError:
                    print("Received an invalid JSON message.")
        finally:
            writer.close()
            await writer.wait_closed()


if __name__ == "__main__":
    data_system = DataSystem(host="127.0.0.1", port=8888)
    asyncio.run(data_system.run())
