def read_skill(skill_name):
    with open(f'skills/{skill_name}.py', 'r') as f:
        lines = f.readlines()
        functions = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0]
                description = None

                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1

                if j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith('"""') or next_line.startswith("'''"):
                        quote = '"""' if next_line.startswith('"""') else "'''"
                        if next_line.count(quote) >= 2:
                            description = next_line.strip(quote).strip()
                        else:
                            doc_lines = [next_line.lstrip(quote)]
                            j += 1
                            while j < len(lines):
                                doc_line = lines[j].strip()
                                if quote in doc_line:
                                    doc_lines.append(doc_line.rstrip(quote).strip())
                                    break
                                doc_lines.append(doc_line)
                                j += 1
                            description = ' '.join(l for l in doc_lines if l)

                functions.append({
                    'name': func_name,
                    'description': description
                })
            i += 1

    return {
        'name': skill_name,
        'functions': functions
    }