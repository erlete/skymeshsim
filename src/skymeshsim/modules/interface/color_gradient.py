#!/usr/bin/env python
# coding: utf-8
# This script demonstrates generating gradients between two specified colors.
# Users can define their start and end colors in HEX format, and the script will display the gradient transition.
# Requirements: numpy, matplotlib
# https://gist.github.com/setuc/c6f0491163ee4622cc03f181fa67c854
import matplotlib.pyplot as plt
import numpy as np


def hex_to_rgb(hex_color):
    """
    Convert hex to RGB.

    Parameters:
    - hex_color: String representing the hexadecimal color code.

    Returns:
    - A tuple of integers representing the RGB values.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def interpolate_color(color_start_rgb, color_end_rgb, t):
    """
    Interpolate between two RGB colors.

    Parameters:
    - color_start_rgb: Tuple of integers representing the starting RGB color.
    - color_end_rgb: Tuple of integers representing the ending RGB color.
    - t: Float representing the interpolation factor between 0 and 1.

    Returns:
    - A tuple representing the interpolated RGB color.
    """
    return tuple(int(start_val + (end_val - start_val) * t) / 255 for start_val, end_val in zip(color_start_rgb, color_end_rgb))

# Example usage:


def get_color_gradient(color_start_hex, color_end_hex):
    color_start_rgb = hex_to_rgb(color_start_hex)
    color_end_rgb = hex_to_rgb(color_end_hex)

    # Generate gradient
    gradient = [interpolate_color(color_start_rgb, color_end_rgb, t)
                for t in np.arange(0, 1, 1/100)]
    # Increase the height of the gradient image
    # gradient = np.array([gradient] * 100)

    # Plot each point in the gradient
    # for i, color in enumerate(gradient):
    #     plt.plot(i, 0, 'o', color=np.array(color))

    # plt.axis('off')
    # plt.show()

    # # Display the gradient
    # plt.figure()
    # plt.imshow(gradient, aspect='auto')
    # plt.axis('off')
    # plt.show()

    return gradient


if __name__ == "__main__":
    get_color_gradient("#00ff07", "#ff0000")
    exit()

    # Define start and end colors
    examples = [
        {"start": "E01A4F", "end": "53B3CB"},
        {"start": "d00000", "end": "3f88c5"},
        {"start": "ffafcc", "end": "a2d2ff"}
    ]

    for example in examples:
        color_start_hex = example["start"]
        color_end_hex = example["end"]
        color_start_rgb = hex_to_rgb(color_start_hex)
        color_end_rgb = hex_to_rgb(color_end_hex)

        # Generate gradient
        gradient = [interpolate_color(color_start_rgb, color_end_rgb, t)
                    for t in np.linspace(0, 1, 256)]
        # Increase the height of the gradient image
        gradient = np.array([gradient] * 100)

        # Display the gradient
        plt.figure(figsize=(10, 2))
        plt.imshow(gradient, aspect='auto')
        plt.axis('off')
        plt.show()
