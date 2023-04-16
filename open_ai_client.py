import os
import openai


class OpenAiClient:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def chat_completion_stream(self, prompt):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )

        for chunk in completion:
            choice = chunk['choices'][0]

            delta = choice['delta']
            if 'content' in delta:
                yield delta['content']

            if choice['finish_reason'] is not None:
                break

    def run_moderation(self, prompt):
        moderation = openai.Moderation.create(
            input=prompt,
        )

        violated_categories = False
        all_categories = moderation.results[0].categories

        for category in moderation.results[0].categories:
            violated_categories |= all_categories[category]

        print(moderation.results[0].categories)

        return violated_categories

