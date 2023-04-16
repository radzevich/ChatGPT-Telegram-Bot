import os
import openai
from context_manager import ContextManager


model = "gpt-3.5-turbo-0301"


class OpenAiClient:
    def __init__(self, context_manager: ContextManager):
        self.context_manager = context_manager
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def run_moderation(content):
        moderation = openai.Moderation.create(input=content)
        all_categories = moderation.results[0].categories

        for category in moderation.results[0].categories:
            if all_categories[category]:
                return True

        return False

    def chat_completion_stream(self, chat_id, content):
        # prepare context
        messages = self.context_manager.get_messages(chat_id)
        messages.append({
            "role": "user",
            "content": content,
        })

        # make request
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True)

        # process response chunks
        tokens = []
        for chunk in completion:
            choice = chunk['choices'][0]

            delta = choice['delta']
            if 'content' in delta:
                token = delta['content']
                tokens.append(token)
                yield token

            if choice['finish_reason'] is not None:
                break

        # store updated context
        messages.append({
            "role": "assistant",
            "content": ''.join(tokens),
        })

        self.context_manager.set_messages(chat_id, messages)
