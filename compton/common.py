from typing import (
    Any
)


def is_hashable(subject: Any) -> bool:
    try:
        hash(subject)
        return True
    except Exception:
        return False


def get_vector(target):
    vector = target.vector

    if not is_hashable(vector):
        raise ValueError(f'{target}.vector is not hashable')

    return vector


# def match_vector(vector, target) -> bool:
#     """Returns `True` if `vector` matches `target`

#     If two vectors has a common sub vector at the beginning, then
#     the shorter one matches the longer one
#     """

#     if vector == target:
#         return True

#     len_v = len(vector)
#     len_t = len(target)

#     if len_v < len_t:
#         return False

#     sub_target = target[:len_v]

#     return vector == sub_target


def set_hierachical(
    target: dict,
    vector: tuple,
    value,
    context: list = []
):
    """Set the value to a dict hirachically

    Args:
        vector (tuple): the length of vector must be larger than 0
    """

    first = vector[0]

    if first in target:
        # There is a conflict
        return False, [*context, first]

    if len(vector) == 1:
        target[first] = value
        return True, None

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
    vector: tuple,
    default: Any = None,
    set_if_not_exists: bool = False
) -> Any:
    """Get a property from a nested dict

    Args:
        target (dict): the dict
        vector (tuple):
        default (Any): if the value does not exist,
        then will return the default value
        no_set (:obj:`bool`, optional)
    """

    last = vector[-1]

    for key in vector[:-1]:
        if key not in target:
            if set_if_not_exists:
                # Then we set the value of key as a dict
                target[key] = {}
                continue
            else:
                return default

        current = target[key]

    if last in current:
        return current[last]

    if set_if_not_exists:
        current[last] = default

    return default


VECTOR_SEPARATOR = ','


def stringify_vector(list_like):
    return f'<{VECTOR_SEPARATOR.join([str(x) for x in list_like])}>'
