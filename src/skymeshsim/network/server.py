import asyncio
import json
from typing import Dict

from .logger import Logger
from .network_component import _BaseNetworkComponent


class SocketServer(_BaseNetworkComponent):
    """Message broker for routing messages between systems and components."""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

        self.clients: Dict[str, asyncio.StreamWriter] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()

        self._logger = Logger(0, "[SocketServer]")

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle client connections and enqueue their messages."""
        try:
            # Identify client:
            client_name = json.loads((await reader.readline()).decode())["component"].strip()
            self.clients[client_name] = writer
            self._logger.log(f"Client {client_name!s} connected.", 1)

            # Read messages from client:
            while True:
                data = await reader.readline()
                if not data:
                    break

                try:
                    message = json.loads(data.decode().strip())
                    await self.message_queue.put((client_name, message))

                except json.JSONDecodeError:
                    self._logger.log(
                        f"Received invalid JSON from {client_name!s}",
                        2
                    )
                    continue
        except asyncio.CancelledError:
            pass
        finally:
            self._logger.log(f"Client {client_name!s} disconnected.", 1)
            self.clients.pop(client_name, None)
            writer.close()
            await writer.wait_closed()

    async def process_messages(self) -> None:
        """Process messages from the queue and route them to appropriate clients."""
        while True:
            client_name, message = await self.message_queue.get()
            self._logger.log(f"Client {client_name!s} says {message}", 0)

            # DataSystem valid messages forwarding:
            if message.get("type") in ("log", "dronestatus") and "DataSystem" in self.clients:
                await self.send_message("DataSystem", message)

            # DroneCommand messages forwarding:
            elif message.get("type") == "cmd":
                # Forward commands to all drones
                for client_name in self.clients:
                    if client_name.startswith("Drone"):
                        await self.send_message(client_name, message)

    async def send_message(self, recipient: str, message: dict) -> None:
        """Send a message to a specific client."""
        if recipient in self.clients:
            writer = self.clients[recipient]
            writer.write((json.dumps(message) + "\n").encode())
            await writer.drain()

    async def run(self) -> None:
        """Start the server and listen for client connections."""
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        self._logger.log(f"Server running on {self.host}:{self.port}", 1)

        async with server:
            await asyncio.gather(server.serve_forever(), self.process_messages())


if __name__ == "__main__":
    socket_server = SocketServer(host="127.0.0.1", port=8888)
    asyncio.run(socket_server.run())
