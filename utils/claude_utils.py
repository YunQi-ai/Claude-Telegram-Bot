from anthropic import AsyncAnthropic
from config import claude_api, claude_default_model

class Claude:
    def __init__(self):
        self.model = claude_default_model
	self.cutoff = 50
        self.temperature = 0.7
        self.max_tokens = 1000
        self.client = AsyncAnthropic(api_key=claude_api)
        self.messages = []

    def reset(self):
        self.messages = []

    def change_model(self, model):
        valid_models = {"claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-2.1", "claude-2.0"}
        if model in valid_models:
            self.model = model
            return True
        return False

    def change_temperature(self, temperature):
        try:
            temperature = float(temperature)
        except ValueError:
            return False
        if 0 <= temperature <= 1:
            self.temperature = temperature
            return True
        return False

    def change_max_tokens(self, max_tokens):
        try:
            max_tokens = int(max_tokens)
        except ValueError:
            return False
        if max_tokens > 0:
            self.max_tokens = max_tokens
            return True
        return False

    async def send_message_stream(self, message):
        self.messages.append({"role": "user", "content": message})
        
        response = await self.client.messages.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True
        )
        
        answer = ""
        async for chunk in response:
            if chunk.type == 'content_block_start':
                content_block = chunk.content_block
            elif chunk.type == 'content_block_delta':
                answer += chunk.delta.text
                yield answer
            elif chunk.type == 'content_block_stop':
                pass

        self.messages.append({"role": "assistant", "content": answer})

