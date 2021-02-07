class Keyboard:
    def __init__(self):
        self._text = "Here's some actions"
        self._keys = ["/Portfolio", "/Anomalies", "/Operations"]

    def keys(self):
        return [{"text": key} for key in self._keys]
    
    def text(self):
        return self._text