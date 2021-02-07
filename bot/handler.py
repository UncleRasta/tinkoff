from .telegram import TelegramClient
from .keyboard import Keyboard
from .exchange import Tinkoff

class Handler:
    def __init__(self, telegram, tinkoff):
        self.telegram = telegram
        self.tinkoff = tinkoff

    @classmethod
    def deserealize(cls, message: str, telegram: TelegramClient, tinkoff: Tinkoff):
        if message.startswith("/start"):
            return MainHandler(telegram, tinkoff)
        if message.startswith("/help"):
            return HelpHandler(telegram, tinkoff)
        if message.startswith("/thanks"):
            return GratitudeHanlder(telegram, tinkoff)
        if message.startswith("/portfolio"):
            return PortfolioHandler(telegram, tinkoff)
        return UnknownHandler(telegram, tinkoff)
    
    def handle(self, chat_id: int, message: str):
        raise NotImplementedError


class MainHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.provide_keyboard(chat_id=chat_id, keyboard=Keyboard)


class HelpHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.send_message(chat_id, text="Here is the list of operations")


class GratitudeHanlder(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.send_message(chat_id, text="My pleasure!")


class UnknownHandler(Handler):
    def handle(self, chat_id: int, message: str):
        self.telegram.send_message(
            chat_id,
            text="Sorry, can't understand you, I'm just an exchange bot but i'm constantly imporving! For now, try again, please.",
        )

class PortfolioHandler(Handler):
    def handle(self, chat_id: int, message: str):
        name, price, income = self.tinkoff.get_portfolio()
        self.telegram.send_message(
            chat_id,
            text= name + ' for ' + str(price) + '\nIncome = ' + str(income),
        )