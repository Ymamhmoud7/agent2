import ollama
from utils import ollama_utils

def message(user_input: str, Model: str, History: list[dict] = [], systemPrompt: str = "", system_prefix: str = "") -> str:
    if ollama_utils.ollama_status() == False:
        print("Ollama is not running. Starting Ollama...")
        ollama_utils.ollama_serve()

    full_system = f"{system_prefix}\n\n{systemPrompt}".strip() if system_prefix else systemPrompt

    response = ollama.chat(
        model=Model,
        messages=[
            {"role": "system", "content": full_system},
            *[
                msg
                for turn in History[-6:]
                for msg in [
                    {"role": "user", "content": turn["user"]},
                    {"role": "assistant", "content": turn["assistant"]},
                ]
            ],
            {"role": "user", "content": user_input},
        ],
        stream=True
    )
    for chunk in response:
        yield chunk['message']['content']