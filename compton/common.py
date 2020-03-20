import asyncio
from typing import (
    Any
)

from enum import Enum


async def background_task(coroutine, logger):
    try:
        await coroutine
    except Exception as e:
        logger.error('background task error: %s', e)


def start_background_task(coroutine, logger):
    asyncio.create_task(
        background_task(coroutine, logger)
    )


def match_vector(vector, target) -> bool:
    """Returns `True` if `vector` matches `target`

    If two vectors has a common sub vector at the beginning, then
    the shorter one matches the longer one
    """

    if vector == target:
        return True

    len_v = len(vector)
    len_t = len(target)

    if len_v > len_t:
        return False

    sub_target = target[:len_v]

    return vector == sub_target


def set_hierachical(
    target: dict,
    vector: tuple,
    value,
    loose: bool,
    context: list = []
):
    """Set the value to a dict hirachically

    Args:
        vector (tuple): the length of vector must be larger than 0
        loose (bool): If `False`, if the target already exists,
        it will treat it as a failure
    """

    first = vector[0]

    if len(vector) == 1:
        # The last item
        if loose or first not in target:
            # Which means it is the last item of the vector,
            # we just set the value
            target[first] = value
            return True, None
        else:
            return False, [*context, first]

    if first in target:
        current = target[first]

        if type(current) is not dict:
            # There is a conflict
            return False, [*context, first]
    else:
        # The next level does not exists, we just create it
        current = {}
        target[first] = current

    return set_hierachical(
        current,
        vector[1:],
        value,
        [*context, first]
    )


def get_hierachical(
    target: dict,
    vector: tuple
) -> Any:
    """Get a property from a nested dict

    Args:
        target (dict): the dict
        vector (tuple):
    """

    for key in vector:
        if key not in target:
            return

        target = target[key]

    return target


def get_partial_hierachical(
    target: dict,
    vector: tuple
) -> Any:
    """Get a property from a nested dict, it will
    return the first non-dict object
    """

    for key in vector:
        if key not in target:
            return

        target = target[key]

        if type(target) is not dict:
            return target


Symbol = str
Payload = object
Vector = tuple


VECTOR_SEPARATOR = ','


def stringify_vector(list_like):
    return f'<{VECTOR_SEPARATOR.join([str(x) for x in list_like])}>'


def stringify(self, name):
    try:
        vector_str = stringify_vector(self.vector)
    except Exception:
        return f'{name}<invalid>'

    return name + vector_str


def is_hashable(subject: Any) -> bool:
    try:
        hash(subject)
        return True
    except Exception:
        return False


def check_vector(vector, target):
    if not isinstance(vector, tuple):
        raise ValueError(
            f'vector of {target} must be a tuple, but got `{vector}`'
        )

    if not is_hashable(vector):
        raise ValueError(f'vector `{vector}` of {target} is not hashable')


class DataType(Enum):
    KLINE = 1


class TimeSpan(Enum):
    DAY = 1
