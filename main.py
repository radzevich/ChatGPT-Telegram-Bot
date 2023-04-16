from context_manager import ContextManager
from open_ai_client import OpenAiClient
from telegram_bot import TelegramBot
import logging


# configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    # set up Telegram client
    context_manager = ContextManager()
    openai_client = OpenAiClient(context_manager)
    bot = TelegramBot(openai_client)
    bot.run()
