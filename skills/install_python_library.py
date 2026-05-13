import subprocess

def install_python_library(library_name):
    try:
        subprocess.check_call(['pip', 'install', library_name])
        print(f'Successfully installed {library_name}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install {library_name}: {e}')