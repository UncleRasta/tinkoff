import os
import requests
from enum import Enum
from typing import Optional
from .keyboard import Keyboard

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TelegramMethods(Enum):
    SendMessage = "sendMessage"

class TelegramClient(metaclass=MetaSingleton):
    def __init__(self, access_token: str = None):
        self._access_token = access_token if access_token else os.environ['TG_TOKEN']
        self._base_url = f"https://api.telegram.org/{self._access_token}"
        self._session = requests.Session()
        
    def send_message(self, chat_id: int, text: str):
        self._send_message({"chat_id": chat_id, "text": text})

    def _send_message(self, payload: dict) -> dict:
        return self._send_request(
            url="/".join((self._base_url, TelegramMethods.SendMessage)), body=payload
        )

    def _send_request(self, url: str, body: dict) -> Optional[dict]:
        try:
            response = self._session.post(url, json=body)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {}

    def provide_keyboard(self, chat_id: int, keyboard: Keyboard):
        self._send_message(
            {
                "chat_id": chat_id,
                "text": keyboard.text(),
                "reply_markup": {"keyboard": [keyboard.keys()]},
            }
        )