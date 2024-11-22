import time

import keyboard
import matplotlib.pyplot as plt
import numpy as np

from .modules.core.drone import Drone
from .modules.core.navigation import Position
from .modules.interface.color_gradient import get_color_gradient

drones = [Drone(Position(0, 0, 0), 100) for _ in range(10)]


def update_positions(drones):
    for drone in drones:
        if drone.energy > 0:
            # Move drone randomly
            drone.position.x += np.random.uniform(-1, 1)
            drone.position.y += np.random.uniform(-1, 1)
            drone.position.z += np.random.uniform(-1, 1)
            # Expend energy
            drone.energy = max(0, drone.energy - np.random.uniform(0.5, 1.5))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def on_press(event):
    if event.name == 'q':
        global running
        running = False


keyboard.on_press(on_press)

gradient = get_color_gradient("#ff0000", "#00ff07")
gradient[0] = (0, 0, 0)
assert len(gradient) == 100
running = True

while running and any(drone.energy > 0 for drone in drones):
    update_positions(drones)

    ax.clear()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

    xs = [drone.position.x for drone in drones]
    ys = [drone.position.y for drone in drones]
    zs = [drone.position.z for drone in drones]
    colors = [gradient[int(drone.energy)] for drone in drones]

    ax.scatter(xs, ys, zs, c=colors)
    plt.draw()
    plt.pause(0.1)
    time.sleep(0.1)

keyboard.unhook_all()
plt.show()
