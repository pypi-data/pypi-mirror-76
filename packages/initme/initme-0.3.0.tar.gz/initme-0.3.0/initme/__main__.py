import sys
import os
from pathlib import Path


def analyze_dir(dir):
    sub_dir_arr = []
    has_python = False
    for fn in os.listdir(dir):
        path = Path(dir,fn)
        if os.path.isdir(path):
            sub_dir_arr.append(path)
        else:
            for suffix in ['.py','.py3','.rpy','.pyt','.xpy','.ipynb']:
                if str(path).endswith(suffix):
                    has_python = True
    return has_python, sub_dir_arr

def init_recursie(dir):
    has_python, subdir_arr = analyze_dir(dir)
    print(has_python, subdir_arr)
    if has_python:
        Path(dir,'__init__.py').touch()
    for subdir in subdir_arr:
        init_recursie(subdir)


if __name__ == '__main__':
    project_dir = os.getcwd()
    if len(sys.argv) > 1:
        project_dir = sys.argv[1]
    print(f'Initializing project in directory: {project_dir}')
    init_recursie(project_dir)
