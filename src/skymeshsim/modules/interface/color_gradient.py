#!/usr/bin/env python
# coding: utf-8
# This script demonstrates generating gradients between two specified colors.
# Users can define their start and end colors in HEX format, and the script will display the gradient transition.
# Requirements: numpy, matplotlib
# https://gist.github.com/setuc/c6f0491163ee4622cc03f181fa67c854
# TODO: Update documentation
import numpy as np

RGBTuple = tuple[int, int, int] | tuple[int, ...]


def hex_to_rgb(hex_color: str) -> RGBTuple:
    """
    Convert hex to RGB.

    Parameters:
    - hex_color: String representing the hexadecimal color code.

    Returns:
    - A tuple of integers representing the RGB values.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def interpolate_color(color_start_rgb: RGBTuple, color_end_rgb: RGBTuple, t):
    """
    Interpolate between two RGB colors.

    Parameters:
    - color_start_rgb: Tuple of integers representing the starting RGB color.
    - color_end_rgb: Tuple of integers representing the ending RGB color.
    - t: Float representing the interpolation factor between 0 and 1.

    Returns:
    - A tuple representing the interpolated RGB color.
    """
    return tuple(
        int(start_val + (end_val - start_val) * t) / 255
        for start_val, end_val in zip(color_start_rgb, color_end_rgb)
    )


def get_color_gradient(color_start_hex: str, color_end_hex: str) -> list[RGBTuple]:
    """Generate a color gradient between two specified colors."""
    gradient = [
        interpolate_color(
            hex_to_rgb(color_start_hex),
            hex_to_rgb(color_end_hex),
            step
        )
        for step in np.arange(0, 1, 1/100)
    ]

    return gradient
