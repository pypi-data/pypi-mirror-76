WILDCARD = "*"

class Value:
    def __init__(self, value, *, tags = list()):
        self._value = value
        self._tags = [WILDCARD, *tags]

    def __get__(self, ins, own):
        return self._value

    def match(self, tag):
        return tag in self._tags

class Config:
    @classmethod
    def raw(cls, tag = WILDCARD):
        config_data = dict()
        for key, value in cls.__dict__.items():
            if isinstance(value, Value) and value.match(tag):
                config_data[key] = value._value
        return config_data
