from litellm import completion


class LLM:
    def invoke(self, messages):
        raise NotImplementedError


class OpenAILLM(LLM):
    def __init__(self, api_key, model='openai/gpt-5', max_tokens=2048):
        self.model = model
        self.api_key = api_key
        self.max_tokens = max_tokens

    def invoke(self, message):
        response = completion(
            api_key=self.api_key,
            model=self.model,
            messages=message,
            max_tokens=self.max_tokens        )
        return response.choices[0].message.content.strip()
