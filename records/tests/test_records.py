from records import *
import pytest


def test_valid_keying():
    foo = AttrDictRecord({"a": 1, "b": 2})
    assert foo.a == 1
    assert foo.b == 2


def test_invalid_keying():
    with pytest.raises(
        InvalidKeyError, match="Invalid key detected in dict update. Invalid keys: ]"
    ):
        foo = AttrDictRecord({"]": 1})


def test_immuatbility():
    with pytest.raises(
        ImmutableError, match="'AttrDictRecord' object does not support item assignment"
    ):
        foo = AttrDictRecord({"a": 1, "b": 2})
        foo.g = 2
