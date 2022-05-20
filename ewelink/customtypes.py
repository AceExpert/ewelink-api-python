from abc import ABCMeta
from typing import Generic, TypeVar

T = TypeVar("T")
V = TypeVar("V")

class Subscriptable(Generic[V, T], metaclass = ABCMeta):

    def __getitem__(self, args: V | tuple[V, ...]) -> T:
        raise NotImplemented

    def __call__(self, *args, **kwds):
        raise NotImplemented