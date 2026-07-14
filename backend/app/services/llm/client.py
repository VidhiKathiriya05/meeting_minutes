from ollama import Client
from app.core.settings import settings

client = Client(host="http://127.0.0.1:11434")


class OllamaClient:

    def generate(self, prompt: str, model: str = None) -> str:

        if model is None:
            model = settings.CHUNK_MODEL

        print("=" * 50)
        print("Model:", model)
        print("Host : http://127.0.0.1:11434")

        try:
            response = client.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ], options={"temperature": 0, "top_p":1,"top_k":1, "seed":42, "num_predict":2048}

            )

            print("\n========== OLLAMA RESPONSE ==========")
            print(response)
            print("====================================")
            print("Ollama connected successfully.")
            return response["message"]["content"]

        except Exception as e:
            print("OLLAMA ERROR:", type(e).__name__)
            print("DETAIL:", repr(e))
            raise