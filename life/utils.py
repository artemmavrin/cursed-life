"""Utility functions."""

import numbers


def check_positive_int(value, name):
    """Check that a function parameter is a positive int.

    Parameters
    ----------
    value : object
        The value of the parameter which should be a positive int.

    name : str
        The name of the parameter in the calling function.

    Returns
    -------
    value : int
        The validated positive integer.

    Raises
    ------
    TypeError
        If `value` is not an integer.

    ValueError
        If `value` is not positive.
    """
    if isinstance(value, numbers.Integral):
        value = int(value)
        if value > 0:
            return value
        else:
            raise ValueError(f"Parameter '{name}' must be positive.")
    else:
        raise TypeError(f"Parameter '{name}' must be an integer.")


def check_probability(value, name):
    """Check that a function parameter is a probability (a float in the interval
    [0, 1]).

    Parameters
    ----------
    value : object
        The value of the parameter which should be a probability.

    name : str
        The name of the parameter in the calling function.

    Returns
    -------
    value : int
        The validated probability.

    Raises
    ------
    TypeError
        If `value` is not a float.

    ValueError
        If `value` is not in the interval [0, 1].
    """
    if isinstance(value, numbers.Real):
        value = float(value)
        if 0. <= value <= 1.:
            return value
        else:
            raise ValueError(f"Parameter '{name}' must between 0 and 1.")
    else:
        raise TypeError(f"Parameter '{name}' must be a float.")
