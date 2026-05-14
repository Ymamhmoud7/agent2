import ollama
from utils import ollama_utils

def message(user_input: str, Model: str, History: list[dict] = [], systemPrompt = "") -> str:
    if ollama_utils.ollama_status() == False:
        print("Ollama is not running. Starting Ollama...")
        ollama_utils.ollama_serve()

    
    context_str = ""
    if History:
        recent = History[-6:] # last 3 turns
        context_str = "\n".join([f"User: {turn['user']}\nAssistant: {turn['assistant']}" for turn in recent])
        context_str = f"Context:\n{context_str}\n\n"

    response = ollama.chat(
        model=Model,
        messages=[
            {"role": "system", "content": systemPrompt},
            *[
                msg
                for turn in History[-6:]
                for msg in [
                    {"role": "user", "content": turn["user"]},
                    {"role": "assistant", "content": turn["assistant"]},
                ]
            ],
            {"role": "user", "content": user_input},  # just the raw message
        ],
        stream=True
        
    )
    for chunk in response:
        yield chunk['message']['content']