import random, asyncio, functools

from typing import Callable, Coroutine, Any, TypeVar, Generic, get_args

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
Callback = Callable[..., Coroutine[None, Any, T]]

def nonce(length: int = 15) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def main(*args: Any, **kwargs: Any) -> Callable[[Callback], T]:
    def decorator(f: Callback) -> T:
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return decorator

def generics(*types: TypeVar):
    def decorator(f: Callable[[T, ...], U]) -> type[type[types]]:
        class _typedfn:
            __types: tuple[type[type], ...]
            def __getitem__(self, _types: type[type]):
                self.__types = _types
                return self

            @functools.wraps(f)
            def __call__(self, *args: Any, **kwds: Any) -> f.__annotations__.get('return', None):
                kwds.update(types = self.__types if isinstance(self.__types, tuple) else tuple([self.__types]))
                return f(*args, **kwds)

        _typedfn.__qualname__ = f.__qualname__
        return _typedfn()
    return decorator


#Should work but doesn't, still keeping it cause simpler implementation
'''
def generics(*types: TypeVar):
    def decorator(f: Callable[[T, ...], U]) -> type[type[types]]:
        class _typedfn(Generic[types]):
            @functools.wraps(f)
            def __new__(cls: type[V], *args, **kwargs) -> f.__annotations__.get('return', None):
                kwargs.update(types = get_args(cls))
                return f(*args, **kwargs)

        _typedfn.__qualname__ = f.__qualname__
        return _typedfn
    return decorator
'''