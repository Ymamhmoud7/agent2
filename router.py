import ollama
from config import ROUTER_MODEL
from utils import ollama_utils
from prompts import ROUTERING_PROMPT

def eval_user_input(user_input: str, Model: str = ROUTER_MODEL, History: list[dict] = []) -> str:
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
            {
                "role": "system",
                "content": ROUTERING_PROMPT.PROMPT
            },
            {
                "role": "user",
                "content": f"Context: {context_str} \n Message: {user_input}\n Label: "
            }
        ],
        options={
            "temperature": 0.0,
            "num_predict": 5
        },
        
    )
    return response['message']['content']