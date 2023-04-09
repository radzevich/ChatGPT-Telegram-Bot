import logging
import traceback
import os

from open_ai_client import OpenAiClient, OpenAiViolatedException
from response_builder import ResponseBuilder
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode
from time import time


class TelegramBot:
    def __init__(self, openai: OpenAiClient):
        self.openai = openai
        self.logger = logging.getLogger('TelegramBot')

        self.application = ApplicationBuilder().token(os.environ['TELEGRAM_TOKEN']).build()
        self.application.add_handler(CommandHandler('ask', self._ask_command_async))
        self.application.add_error_handler(self.error_handler_context)

    def run(self):
        self.application.run_polling()

    async def _ask_command_async(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                                 text="Loading...")

        last_message_time = time()
        response_builder = ResponseBuilder()

        try:
            openai_response = self.openai.chat_completion_stream(prompt=update.message.text)

            for (token, is_last) in openai_response:
                response_builder.append_token(token)

                now = time()
                if not is_last and now - last_message_time < 1:
                    continue

                # edit message in Telegram
                last_message_time = now
                try:
                    message = await context.bot.edit_message_text(text=response_builder.to_string(),
                                                                  chat_id=message.chat_id,
                                                                  message_id=message.message_id,
                                                                  parse_mode=ParseMode.MARKDOWN_V2)
                except Exception as ex:
                    self.logger.error('message: %s\ntrace: %s', str(ex), traceback.format_exc())
        except OpenAiViolatedException as ex:
            await context.bot.edit_message_text(text=str(ex),
                                                chat_id=message.chat_id,
                                                message_id=message.message_id)

    async def error_handler_context(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=context.error)


