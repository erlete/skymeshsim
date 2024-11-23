# Register parameters for the script:
param (
    [int]$droneCount = 1
)

# Define the commands to run in each terminal:
$commands = @(
    "python -m skymeshsim.network.server",
    "python -m skymeshsim.network.data_system"
)

# Add the specified number of drone commands:
for ($i = 1; $i -le $droneCount; $i++) {
    $commands += "python -m skymeshsim.network.drone $i"
}

# Control system command must be the last one:
$commands += "python -m skymeshsim.network.control_system"

# Loop through the commands and open a new terminal for each:
foreach ($command in $commands) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal -WorkingDirectory $PWD -PassThru
}
