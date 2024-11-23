"""Main module for the package.

This module is responsible for running the server script in the appropriate
platform. It provides a bridge between the package and the user, allowing the
user to run the server script from the command line.

This module is not intended to be imported by other modules in the package.

Author:
    Paulo Sanchez (@erlete)
"""


import os
import subprocess
import sys

if __name__ == "__main__":
    if sys.platform == "win32":
        SCRIPT_PATH = os.path.join(os.path.dirname(
            __file__), "scripts", "run_windows_server.ps1")
        args = sys.argv[1:]
        subprocess.run(
            ["powershell", "-File", SCRIPT_PATH] + args,
            shell=True,
            check=True
        )

    else:
        print(f"This module cannot be run in your platform ({sys.platform}).")
