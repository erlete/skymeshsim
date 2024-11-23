param (
    [int]$droneCount = 1
)

# Define the commands to run in each terminal
$commands = @(
    "python -m skymeshsim.network.server",
    "python -m skymeshsim.network.data_system",
    "python -m skymeshsim.network.control_system"
)

# Add the specified number of drone commands
for ($i = 1; $i -le $droneCount; $i++) {
    $commands += "python -m skymeshsim.network.drone $i"
}

# Define a counter for window positions
$position = 0

# Loop through the commands and open a new terminal for each
foreach ($command in $commands) {
    # Calculate window position (optional, adjust as needed)
    $left = $position * 300
    $top = $position * 100

    # Open a new terminal window and run the command
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal -WorkingDirectory $PWD -PassThru
    $position++
}
