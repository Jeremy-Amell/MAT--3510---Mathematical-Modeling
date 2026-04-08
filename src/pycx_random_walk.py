from math import cos, pi, sin
import random

import matplotlib.pyplot as plt

import pycxsimulator


position = [0.0, 0.0]
history = []


def initialize():
    """Minimal PyCX example: a 2D random walk."""
    global position, history
    position = [0.0, 0.0]
    history = [tuple(position)]


def observe():
    plt.cla()
    x_values, y_values = zip(*history)
    x_padding = max(2.0, max(abs(value) for value in x_values) + 1.0)
    y_padding = max(2.0, max(abs(value) for value in y_values) + 1.0)

    plt.plot(x_values, y_values, color="steelblue", linewidth=1.5)
    plt.scatter(x_values[-1], y_values[-1], color="darkred", s=45)
    plt.xlim(-x_padding, x_padding)
    plt.ylim(-y_padding, y_padding)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True, alpha=0.3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"PyCX Random Walk (step {len(history) - 1})")


def update():
    """Advance the walk by one random step."""
    angle = random.random() * 2.0 * pi
    position[0] += cos(angle)
    position[1] += sin(angle)
    history.append(tuple(position))


if __name__ == "__main__":
    pycxsimulator.GUI(title="PyCX Random Walk", interval=0).start(
        [initialize, observe, update]
    )