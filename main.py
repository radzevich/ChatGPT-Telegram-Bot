from open_ai_client import OpenAiClient
from telegram_bot import TelegramBot
import logging


# configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    # set up OpenAI client
    openai = OpenAiClient()

    # set up Telegram client
    bot = TelegramBot(openai)
    bot.run()
