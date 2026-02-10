from ..strict import *
import pytest


def test_strict_abc_meta():
    class Foo(metaclass=StrictABCMeta):
        @strictabstract
        def bar(self):
            pass

        # @strictabstract
        def baz(self, a):
            pass

    class ConFooPass(Foo):
        def bar(self):
            print("happy")

        def baz(self, a):
            print(a)

    assert ConFooPass()

    class ConFooPass(Foo):
        @classmethod
        def bar(self):
            print("happy")

        def baz(self, a):
            print(a)

    with pytest.raises(MissingMethodsError):

        class ConFooFailMissing(Foo):
            pass

    with pytest.raises(MissmatchedSignaturesError):

        class ConFooFailSig(Foo):
            def bar(cls):
                print("happy")

            def baz(self, A):
                print(A)
