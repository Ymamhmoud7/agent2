import ollama
from config import ROUTER_MODEL
from utils import ollama_utils
from prompts import ROUTERING_PROMPT

def eval_user_input(user_input: str, Model: str = ROUTER_MODEL) -> str:
    if ollama_utils.ollama_status() == False:
        print("Ollama is not running. Starting Ollama...")
        ollama_utils.ollama_serve()
    else:
        print("Ollama is already running.")
    
    response = ollama.chat(
        model=ROUTER_MODEL,
        messages=[
            {
                "role": "system",
                "content": ROUTERING_PROMPT.Prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return response['message']['content']