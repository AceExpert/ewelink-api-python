import typing

class Object(dict):
    def __init__(self, data: typing.Dict[typing.Any, typing.Any] = {}):
        super().__init__(data)
        try:
            self.__recurse_to_self()
        except RecursionError:
            pass
    def __getattr__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            raise AttributeError(e)
    def __setattr__(self, name: str, value: typing.Any) -> None:
        return super().__setitem__(name, Object(value) if type(value) == dict else value)
    def __delattr__(self, name: str):
        return super().pop(name)
    def __setitem__(self, k, value) -> None:
        return super().__setitem__(k, Object(value) if type(value) == dict else value)
    def __iter__(self):
        return super().items()
    def map(self, func: typing.Callable):
        _copy_data = super().copy()
        for key, val in super().items():
            _copy_data.__setitem__(key, func((key, val)))
        return _copy_data
    def map_key(self, func: typing.Callable):
        _copy_data = super().copy()
        for key, val in super().items():
            _copy_data.__setitem__(func((key, val)), _copy_data.pop(key))
        return _copy_data
    def map_items(self, func: typing.Callable):
        _copy_data = {}
        for key, val in super().items():
            item = func((key, val))
            _copy_data.__setitem__(item[0], item[1])
        return _copy_data
    def __recurse_to_self(self):
        for key, value in super().items():
            if type(value) == dict:
                super().__setitem__(key, Object(value))
            if type(value) == list:
                l = list(map(Object, value.copy()))
                super().__setitem__(key, l)