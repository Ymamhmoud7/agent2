import importlib.util
import os

SKILLS_DIR = os.path.join(os.path.dirname(__file__), 'skills')

def load_skill_functionality(func_name: str):
    skill_path = os.path.join(SKILLS_DIR, f"{func_name}.py")
    if not os.path.isfile(skill_path):
        raise FileNotFoundError(f"Skill '{func_name}' not found in skills directory.")
    
    spec = importlib.util.spec_from_file_location(func_name, skill_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, func_name):
        raise AttributeError(f"Skill file '{func_name}.py' has no function named '{func_name}'")
 
    return getattr(module, func_name)

def executor(function_name: str, args: dict):
    try:
        func = load_skill_functionality(function_name)
        return func(**args)
    except FileNotFoundError as e:
        return {"success": False, "error": str(e)}
    except AttributeError as e:
        return {"success": False, "error": str(e)}
    except TypeError as e:
        return {"success": False, "error": f"Wrong args for '{function_name}': {e}"}
    except Exception as e:
        return {"success": False, "error": f"Skill '{function_name}' raised: {e}"}
 