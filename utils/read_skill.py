def read_skill(skill_name):
    with open(f'skills/{skill_name}.py', 'r') as f:
        file = f.read()
        functions = []
        for line in file.splitlines():
            if line.startswith('def '):
                func_name = line.split('def ')[1].split('(')[0]
                functions.append(func_name)
        
        dict = {
            'name': skill_name,
            'functions': functions
        }
    return dict
