# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    from typing import Union, List, Literal, Annotated, TypeVar
    import numpy as np
    import numpy.typing as npt

T = _ext.TypeVar("T")

Vector2 = _ext.Annotated[_ext.npt.NDArray[T], _ext.Literal[2]]
Vector3 = _ext.Annotated[_ext.npt.NDArray[T], _ext.Literal[3]]
Vector4 = _ext.Annotated[_ext.npt.NDArray[T], _ext.Literal[4]]

Vector2f = Vector2[_ext.np.float32]
Vector3f = Vector3[_ext.np.float32]
Vector4f = Vector4[_ext.np.float32]
Vector2i = Vector2[_ext.np.int32]
Vector3i = Vector3[_ext.np.int32]
Color = Vector4f
UV = Vector2f

Vector2fCompat = _ext.Union[Vector2f, _ext.List[float]]
Vector3fCompat = _ext.Union[Vector3f, _ext.List[float]]
Vector4fCompat = _ext.Union[Vector3f, _ext.List[float]]

# TODO: Use numpy properly...

def as_vector2f(v:Vector2fCompat)->Vector2f:
    """ Ensures this value is a vec2f, missing values are filled with zero """
    array = _ext.np.array(v, dtype=_ext.np.float32)
    array.resize(2, refcheck=False)
    return array

def as_vector3f(v:Vector3fCompat)->Vector3f:
    """ Ensures this value is a vec3f, missing values are filled with zero """
    array = _ext.np.array(v, dtype=_ext.np.float32)
    array.resize(3, refcheck=False)
    return array

def as_vector4f(v:Vector4fCompat)->Vector4f:
    """ Ensures this value is a vec4f, missing values are filled with zero """
    array = _ext.np.array(v, dtype=_ext.np.float32)
    array.resize(4, refcheck=False)
    return array
