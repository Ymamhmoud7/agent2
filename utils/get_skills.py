import os

def get_skills():
    skills_dir = os.path.join(os.path.dirname(__file__), '..', 'skills')
    skill_files = [f for f in os.listdir(skills_dir) if f.endswith('.py') and f != '__init__.py']
    
    skills = {}
    for skill_file in skill_files:
        skill_name = skill_file[:-3]  # Remove .py extension
        module_path = f'skills.{skill_name}'
        try:
            module = __import__(module_path, fromlist=[skill_name])
            skills[skill_name] = module
        except ImportError as e:
            print(f'Failed to import {module_path}: {e}')
    
    return skills