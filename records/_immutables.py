from collections import OrderedDict
from keyword import iskeyword, issoftkeyword
from typing import Any


class InvalidKeyError(AttributeError):
    def __ini__(self, msg: str) -> None:
        super().__init__(msg)


class ImmutableError(TypeError):
    def __ini__(self, msg: str) -> None:
        super().__init__(msg)


class AttrDictRecord(OrderedDict):

    def __init__(self, iterable: Any) -> None:
        super().__init__(iterable)
        invalid = [
            attr
            for attr in map(str, self.keys())
            if iskeyword(attr) or issoftkeyword(attr) or not attr.isidentifier()
        ]
        if invalid:
            msg = f'Invalid key detected in dict update. Invalid keys: {", ".join(invalid)}'
            raise InvalidKeyError(msg)
        self.__dict__.update(self.items())

    def __setattr__(self, name, value):
        raise ImmutableError(
            f"'{self.__class__.__name__}' object does not support item assignment"
        )


__all__ = [
    "InvalidKeyError",
    "ImmutableError",
    "AttrDictRecord",
]
