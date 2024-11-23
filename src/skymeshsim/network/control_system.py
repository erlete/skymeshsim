import asyncio

from .messages import ClientIdentificationMessage, CommandMessage
from .network_component import _BaseNetworkComponent


class ControlSystem(_BaseNetworkComponent):
    """Sends user commands to the server."""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    async def get_user_input(self) -> str:
        """Asynchronously get user input."""
        print("> ", end="", flush=True)
        return await asyncio.get_event_loop().run_in_executor(None, input)

    async def run(self) -> None:
        """Connect to the server and send user commands."""
        _, writer = await asyncio.open_connection(self.host, self.port)
        await ClientIdentificationMessage(
            component="ControlSystem",
            writer=writer
        ).send()

        print("ControlSystem connected. Type commands (e.g., 'moveto 10, 20').")
        try:
            while True:
                command = await self.get_user_input()
                if command.strip().lower() == "exit":
                    print("Exiting ControlSystem...")
                    break

                # Prepare the command as a JSON object
                if command.lower().startswith("moveto"):
                    # Example: Move to <x>, <y>
                    await CommandMessage(
                        command="moveto",
                        target=tuple(
                            map(float, command.split("moveto ")[1].split(","))
                        ),
                        writer=writer
                    ).send()
                else:
                    print("Unknown command format. Only 'CMD:' commands are allowed.")
        except asyncio.CancelledError:
            print("ControlSystem interrupted.")
        finally:
            writer.close()
            await writer.wait_closed()


if __name__ == "__main__":
    control_system = ControlSystem(host="127.0.0.1", port=8888)
    asyncio.run(control_system.run())
