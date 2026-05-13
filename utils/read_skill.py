def read_skill(skill_name):
    with open(f'skills/{skill_name}.py', 'r') as f:
        return f.read()
