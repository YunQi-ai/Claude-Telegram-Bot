from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT
from config import claude_api, claude_default_model

class Claude:
    def __init__(self):
        self.model = claude_default_model  # Use the default model from config
        self.temperature = 0.7
        self.cutoff = 50
        self.client = AsyncAnthropic(api_key=claude_api)
        self.prompt = ""

    def reset(self):
        self.prompt = ""

    def revert(self):
        self.prompt = self.prompt[: self.prompt.rfind(HUMAN_PROMPT)]

    def change_model(self, model):
        # Updated list of valid models
        valid_models = {"claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-2.1", "claude-instant-1.2"}
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

    def change_cutoff(self, cutoff):
        try:
            cutoff = int(cutoff)
        except ValueError:
            return False
        if cutoff > 0:
            self.cutoff = cutoff
            return True
        return False

    async def send_message_stream(self, message):
        self.prompt = f"{self.prompt}{HUMAN_PROMPT} {message}{AI_PROMPT}"
        response = await self.client.completions.create(
            prompt=self.prompt,
            model=self.model,
            max_tokens_to_sample=100000,
            temperature=self.temperature,
            stream=True
        )
        answer = ""
        async for completion in response:
            if completion.stop_reason:
                break
            answer += completion.completion
            yield answer
        self.prompt = f"{self.prompt}{answer}"
