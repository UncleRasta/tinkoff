class Keyboard:
    _text = None
    _keys = None

    @classmethod
    def keys(cls):
        return [{"text": key} for key in cls._keys]

    @classmethod
    def text(cls):
        return self._text


class HelperKeyboard(Keyboard):
    _text = "Here's some actions"
    _keys = ["Portfolio", "Anomalies", "Operations"]
