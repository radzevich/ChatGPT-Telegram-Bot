import logging
import traceback
from open_ai_client import OpenAiClient
from telegram.constants import ParseMode
from enum import Enum
from time import time
from response_formatter import to_markdown2_string


class Chat:
    class UserType(Enum):
        USER = 1
        CHAT_GPT = 2

    def __init__(self, chat_id, bot, openai: OpenAiClient):
        self.chat_id = chat_id
        self.bot = bot
        self.openai = openai
        self.messages = []
        self.logger = logging.getLogger('Chat')

    async def send_message_async(self, text):
        message = await self.bot.send_message(chat_id=self.chat_id,
                                              text="Loading...")

        for answer in self.answer_stream(text):
            try:
                message = await self.bot.edit_message_text(text=answer,
                                                           chat_id=message.chat_id,
                                                           message_id=message.message_id,
                                                           parse_mode=ParseMode.MARKDOWN_V2)
            except Exception as ex:
                self.logger.error('message: %s\ntrace: %s', str(ex), traceback.format_exc())

    def answer_stream(self, question):
        self.messages.append((Chat.UserType.USER, question))

        # check that request doesn't violates rules
        if self.openai.run_moderation(prompt=question):
            yield "Sorry, we can\'t fulfill your request because it violates the rules of the service 😢"
            return

        last_message_time = time()
        tokens = []

        # process response stream
        for token in self.openai.chat_completion_stream(prompt=question):
            tokens.append(token)

            now = time()
            if now - last_message_time >= 1:
                last_message_time = now
                yield to_markdown2_string(''.join(tokens))

        raw_response = ''.join(tokens)
        yield to_markdown2_string(raw_response)

        self.messages.append((Chat.UserType.CHAT_GPT, raw_response))
