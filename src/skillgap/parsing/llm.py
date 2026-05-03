from llama_cpp import Llama


class LLMClient:
    def __init__(self, model_name: str):
        self.load_model(model_name)

    def load_model(self, model_name: str) -> None:
        self.llama = Llama(
            model_path=model_name,
            n_ctx=4096,
            n_threads=4,
            verbose=False,
        )

    def clean_response(self, response: str) -> str:
        # parfois le LLM renvoie du texte avant ou après le JSON, on veut juste le JSON
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return response[start:end]
        else:
            raise ValueError("Le LLM n'a pas renvoyé un JSON valide.")

    def generate(self, prompt: str, max_new_tokens: int = 300) -> str:
        response = self.llama.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_new_tokens,
            temperature=0.0,
        )

        output = response["choices"][0]["message"]["content"]
        # assertion for mypy
        assert isinstance(output, str)
        return self.clean_response(output)
