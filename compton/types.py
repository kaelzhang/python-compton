from .common import (
    stringify_vector
)


Symbol = str
Payload = object


class Vector(tuple):
    __str__ = stringify_vector


class DataType:
    KLINE = 1


class TimeSpan:
    DAY = 1
