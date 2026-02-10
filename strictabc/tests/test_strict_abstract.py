from ..strict import *
import pytest


@pytest.fixture
def setup():
    class Foo(metaclass=StrictABCMeta):
        @strictabstract
        def bar(self):
            pass

        # @strictabstract
        def baz(self, a):
            pass

    return Foo


def test_strict_abc_meta(setup):

    Foo = setup

    class ConFooPass(Foo):
        def bar(self):
            print("happy")

        def baz(self, a):
            print(a)

    assert ConFooPass()

    class ConFooPassClass(Foo):
        @classmethod
        def bar(self):
            print("happy")

        def baz(self, a):
            print(a)

    assert ConFooPassClass()


def test_fail_missing(setup):
    Foo = setup
    with pytest.raises(StrictAbstractError):

        class ConFooFailMissing(Foo):
            pass


def test_fail_missmatch(setup):
    Foo = setup
    with pytest.raises(StrictAbstractError):

        class ConFooFailSig(Foo):
            def bar(cls):
                print("happy")

            def baz(self, A):
                print(A)
