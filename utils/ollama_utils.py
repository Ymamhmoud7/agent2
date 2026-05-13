import subprocess
import requests

def get_ollama_models() -> list:
    result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Error getting Ollama models: {result.stderr}")
    
    models = []
    for line in result.stdout.splitlines():
        if line.strip() and not line.startswith("NAME"):
            model_name = line.split()[0]
            models.append(model_name)
    
    return models


def get_ollama_model_info(model_name: str) -> dict:
    result = subprocess.run(['ollama', 'inspect', model_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Error inspecting Ollama model '{model_name}': {result.stderr}")
    
    info = {}
    for line in result.stdout.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            info[key.strip()] = value.strip()
    
    return info

def install_ollama_model(model_name: str):
    result = subprocess.run(['ollama', 'pull', model_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Error installing Ollama model '{model_name}': {result.stderr}")
    print(f"Model '{model_name}' installed successfully.")

def ollama_serve(model_name: str = None):
    result = subprocess.run(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Error serving Ollama")
    print(f"Ollama is now serving.")

def ollama_status(host: str = "http://localhost:11434") -> bool:
    try:
        response = requests.get(f"{host}/api/tags", timeout=3)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False