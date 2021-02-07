from .telegram import TelegramClient
from .keyboard import HelperKeyboard


class Handler:
    def __init__(self, telegram):
        self.telegram = telegram

    @classmethod
    def deserealize(cls, message: str, telegram: TelegramClient):
        if message.startswith("/start"):
            return MainHandler(telegram)
        if message.startswith("/help"):
            return HelpHanlder(telegram)
        if message.startswith("/thanks"):
            return GratitudeHanlder(telegram)
        return UnknownHandler(telegram)

    def handle(self, chat_id: int, message: str):
        raise NotImplemented


class MainHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.provide_keyboard(chat_id=chat_id, keyboard=HelperKeyboard)


class HelpHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.send_message(chat_id, text="Here is the list of operations")


class GratitudeHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.send_message(chat_id, text="My pleasure!")


class UnknownHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.send_message(
            chat_id,
            text="Sorry, can't understand you, I'm just an exchange bot but i'm constantly imporving! For now, try again, please.",
        )
