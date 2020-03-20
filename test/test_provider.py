import pytest
from compton import (
    Provider,
    Orchestrator
)

from .types import (
    SimpleReducer
)


def test_check():
    class A:
        pass

    with pytest.raises(
        ValueError,
        match='must be an instance of Provider'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(A())


def test_str():
    class InvalidProvider(Provider):
        @property
        def vector(self):
            return 1

        def init():
            pass

        def when_update():
            pass

    assert str(InvalidProvider()) == 'provider<invalid>'

    class ValidVectorProvider(Provider):
        @property
        def vector(self):
            return (1, 2)

        def init():
            pass

        def when_update():
            pass

    assert str(ValidVectorProvider()) == 'provider<1,2>'
