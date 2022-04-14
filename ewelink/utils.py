import random, asyncio

from typing import Callable, Coroutine, Any, TypeVar

T = TypeVar("T")
Callback = Callable[..., Coroutine[None, Any, T]]

def nonce(length: int = 15) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def main(*args: Any, **kwargs: Any) -> Callable[[Callback], T]:
    def decorator(f: Callback) -> T:
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return decorator
