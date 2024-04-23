# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
"""Color specific algorithms
"""
class _ext:
    """ External Dependencies """
    from typing import List, Union
    from numpy import typing as npt
    from met_viewport_utils.algorithm import types


def parse_color(color:_ext.Union[float, str, _ext.types.Vector3fCompat], alpha:float=None) ->_ext.npt.NDArray:
    """Given a color as vector, float or hex, return a color vector

    Args:
        color (Union[float, str, _Vector, _List[float]]):
        alpha(float): alpha to use

    Raises:
        ValueError: If color is a vec2

    Returns:
        Vector
    """
    alpha_value:float = alpha if alpha is not None else 1.0
    if isinstance(color, int):
        return _ext.types.as_vector4f((color, color, color, alpha))
    if isinstance(color, str):
        hex = color.strip("#")
        if len(hex) == 6:
            color = [int(hex[i:i+2], 16)/255.0  for i in (0, 2, 4)] + [alpha_value]
        else:
            color = [int(hex[i:i+2], 16)/255.0  for i in (0, 2, 4, 6)]
            if alpha is not None:
                color[3] = alpha_value
    if len(color) == 2:
        raise ValueError("Invalid color, requires 3 or 4 channels, got 2")
    elif len(color) == 3:
        return _ext.types.as_vector4f((*color, 1.0))
    else:
        return _ext.types.as_vector4f(color)
