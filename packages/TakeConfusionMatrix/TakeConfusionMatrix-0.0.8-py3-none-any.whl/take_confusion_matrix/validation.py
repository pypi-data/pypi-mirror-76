import numpy as np

from typing import Union, List, Dict, Any


def check_value_mapped(mapper: Dict, values: Union[List, np.ndarray]):
    """Check that all values passed were mapped

    Checks whether the values passed were previously mapped.

    Parameters
    ----------
    mapper : dict
        Dictionary with the values previously mapped.

    values : 1d array-like
        Values to be validated.

    Raises
    -------
    AssertionError
        If the values don't correspond to the mapped ones.
    """

    for value in values:
        assert mapper.get(value, False), (f"Found value `{value}` while "
                                          f"the expected ones were {list(mapper.keys())}.")


def check_array_size(x: Any, name: str, min_size: Union[int, float]):
    """Validate scalar parameter size.

    Parameters
    ----------
    x : object
        The scalar parameter to validate.

    name : str
        The name of the parameter to be printed in error messages.

    min_size : int or float
        The minimum valid size the parameter can take. 

    Raises
    -------
    AssertionError
        If object's size is smaller than mininum size.
    """

    size = len(x)
    assert size >= min_size, (f"Size of `{name}` = {size}"
                              f", must be >= {min_size}")
