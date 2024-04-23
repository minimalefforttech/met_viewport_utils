# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
""" linear algebra functions """


def lerp(a:float, b:float, t:float) -> float:
    """Standard lerp function
    interpolates between a and b by t
    where t is between 0 and 1

    Args:
        a (float):
        b (float):
        t (float):

    Returns:
        float
    """
    return (1 - t) * a + t * b


def inverse_lerp(a: float, b: float, v: float) -> float:
    """Opposite of lerp, returns t value from value(v) between a and b

    Args:
        a (float):
        b (float):
        v (float):

    Returns:
        float t
    """
    if b == a:
        return 0.0
    return (v - a) / (b - a)


def scale_number(a:float, a_min:float, a_max:float, b_min:float=0.0, b_max:float=1.0):
    """Scales (a) from within range(a_min->a_max) to relevant value between (b_min->b_max)

    Args:
        a (float):
        a_min (float):
        a_max (float):
        b_min (float, optional):. Defaults to 0.0.
        b_max (float, optional):. Defaults to 1.0.

    Returns:
        float
    """
    if a_min == a_max:
        return b_min
    return b_min + ((a - a_min) / (a_max - a_min)) * (b_max - b_min)


def clamp(value:float, min_value:float, max_value:float):
    """Clamps a value between two other values

    Args:
        value (float):
        min_value (float):
        max_value (float):

    Returns:
        float:
    """
    return min(max_value, max(min_value, value))
