import os

def print_directory_structure(root_dir, indent=''):
    files = os.listdir(root_dir)
    for file in files:
        path = os.path.join(root_dir, file)
        print(indent + file)
        if os.path.isdir(path):
            print_directory_structure(path, indent + '    ')

# Replace '.' with the path you want to list
print_directory_structure('.')
