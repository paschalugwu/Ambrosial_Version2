import os

def print_directory_structure(root_dir, indent=''):
    try:
        # List all items in the directory
        items = os.listdir(root_dir)
    except PermissionError:
        print(indent + '[Permission Denied]')
        return
    except Exception as e:
        print(indent + f'[Error: {e}]')
        return
    
    for item in items:
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            print(indent + item + '/')
            print_directory_structure(path, indent + '    ')
        else:
            print(indent + item)

# Replace '.' with the path you want to list
print_directory_structure('.')
