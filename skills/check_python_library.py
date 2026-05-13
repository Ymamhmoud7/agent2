import subprocess

def check_python_library(library_name):
    try:
        subprocess.check_call(['pip', 'show', library_name])
        print(f'{library_name} is installed.')
    except subprocess.CalledProcessError:
        print(f'{library_name} is not installed.')

def list_python_libraries():
    try:
        result = subprocess.check_output(['pip', 'list'], text=True)
        print('Installed Python libraries:')
        print(result)
    except subprocess.CalledProcessError as e:
        print(f'Failed to list Python libraries: {e}')