from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple, Iterable
from inspect import getmembers, signature
from collections import namedtuple

_sentinel = object()

miss_matched_sigs = namedtuple(
    "miss_matched_sigs", ["method_name", "good_sig", "bad_sig"]
)

__strict_signature__ = "__strict_signature__"


class MissingMethodsError(AttributeError):
    def __init__(self, name: str, missing: List[str]):
        msg = f"Missing methods from <{name}>: {missing}"
        super().__init__(msg)


class MissmatchedSignaturesError(AttributeError):
    def __init__(self, name: str, bad_sigs: List[miss_matched_sigs]):
        msg = f"Bad signatures detected in <{name}>: {bad_sigs}"
        super().__init__(msg)


def strictabstract(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.  abstractmethod() may be used to declare
    abstract methods for properties and descriptors.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractmethod
            def my_abstract_method(self, arg1, arg2, argN):
                ...
    """
    sig = signature(funcobj)
    setattr(funcobj, __strict_signature__, sig)
    funcobj.__isabstractmethod__ = True
    return funcobj


class StrictABCMeta(ABCMeta):
    def __new__(mcls, name, bases, classdict, /, **kwargs):

        cls = super().__new__(mcls, name, bases, classdict, **kwargs)

        mcls._check_bases(mcls, bases, classdict)

        return cls

    def _check_bases(mcls, bases, classdict):
        concrete_methods = dict(
            (method_name, method)
            for method_name, method in classdict.items()
            if callable(method)
        )
        for base in bases:
            base_methods = dict(
                (method_name, method)
                for method_name, method in vars(base).items()
                if callable(method) and method_name in base.__abstractmethods__
            )
            mcls._check_missing(mcls, base_methods, classdict)
            mcls._check_missmatch(mcls, base_methods, classdict)

    def _check_missing(mcls, base_methods, classdict):
        missing = []
        for method_name in base_methods:
            concrete_method = classdict.get(method_name, _sentinel)
            if concrete_method is _sentinel:
                missing.append(method_name)
        if missing:
            raise MissingMethodsError(mcls.__name__, missing)

    def _check_missmatch(mcls, base_methods, classdict):
        mbad_sigs = []
        for method_name, method in base_methods.items():
            concrete_method = classdict.get(method_name, _sentinel)
            base_sig = getattr(method, __strict_signature__)
            concrete_sig = signature(concrete_method)
            if concrete_sig != base_sig:
                bad_sig = miss_matched_sigs(
                    method_name=classdict["__qualname__"],
                    good_sig=base_sig,
                    bad_sig=concrete_sig,
                )
                mbad_sigs.append(bad_sig)
        if mbad_sigs:

            raise MissmatchedSignaturesError(mcls.__name__, mbad_sigs)


__all__ = [
    "StrictABCMeta",
    "strictabstract",
    "MissingMethodsError",
    "MissmatchedSignaturesError",
]
