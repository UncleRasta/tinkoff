from typing import Tuple
from flask import Flask, request

from bot.handler import Handler
from bot.telegram import TelegramClient
from bot.exchange import Tinkoff


app = Flask(__name__)
telegram_client = TelegramClient()


@app.route("/", methods=["POST"])
def index():
    chat_id, message_text = parse_request(request=request.get_json())
    handler = Handler.deserealize(message_text, telegram_client, Tinkoff)
    handler.handle(chat_id, message_text)

def parse_request(request: dict) -> Tuple[int, str]:
    message = request["message"]
    chat = message["chat"]
    return (chat.get("id"), message.get("text").lower())


if __name__ == "__main__":
    app.run()