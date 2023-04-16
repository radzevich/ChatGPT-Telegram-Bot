from cache import LRUCache
from tokenizer import num_tokens_from_messages


class ContextManager:
    def __init__(self):
        self.cache = LRUCache(capacity=10000)

    def set_messages(self, chat_id, messages):
        num_of_tokens = num_tokens_from_messages(messages)
        while len(messages) > 0 and num_of_tokens > 4096:
            messages.pop(0)
            num_of_tokens = num_tokens_from_messages(messages)

        self.cache.set(chat_id, messages)

    def get_messages(self, chat_id):
        messages = self.cache.get(chat_id)
        if messages is not None:
            return messages

        print("CACHE_MISS")
        return []
