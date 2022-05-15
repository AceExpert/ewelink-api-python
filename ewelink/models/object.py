from typing import Any, Generator

class Object(dict):
    __name__: str = "Object"
    def __init__(self, data: dict[Any, Any], name: str = "Object") -> None:
        super().__init__(data)
        self.__name__ = name
        for key, value in super().items():
            if isinstance(value, dict):
                self[key] = Object(value, name = key.title() if isinstance(key, str) else "Object")
            if isinstance(value, list):
                self[key] = [Object(item) if isinstance(item, (dict, list)) else item for item in value]

    def __repr__(self) -> str:
        _fmt = ''
        for k, v in super().items():
            _fmt += f"    {k} = {v!r}\n"
        return "{0}({1})".format(self.__name__, '\n'+_fmt if _fmt else '')

    __str__ = __repr__

    def __getattr__(self, key: str) -> Any:
        return super().get(key, None)
    
    def __setattr__(self, _k: str, _v: Any) -> None:
        if _k == '__name__':
            return super().__setattr__(_k, _v)
        elif _k in super().keys():
            return super().__setitem__(_k, Object(_v))
        raise NotImplementedError("This is read only.")

    def __iter__(self) -> Generator[Any, None, None]:
        return super().items()
