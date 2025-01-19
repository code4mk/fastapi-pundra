import os

# Base path
def base_path(path_name = None):
    if path_name:
        return os.path.join(os.getcwd(), path_name)
    else:
        return os.getcwd()

# App path
def app_path(path_name = None):
    base_path = base_path('app')
    
    if path_name:
        return os.path.join(base_path, path_name)
    else:
        return base_path
    
# Template path
def template_path(path_name = None):
    return os.path.join(app_path('templates'), path_name)