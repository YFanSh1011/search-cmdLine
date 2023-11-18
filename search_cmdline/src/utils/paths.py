import os
from pkg_resources import resource_filename

def get_file_path(filename):
    if (os.getenv('ENV') == 'DEV'):
        # If being launched without packaging, use direct path
        _working_dir = os.getcwd()
        return os.path.join(_working_dir, "search_cmdline", "configs", filename)
    else:
        # Construct the full path for the JSON file
        return resource_filename('search_cmdline', f'configs/{filename}')
        

SEARCH_ENGINES = get_file_path('search_engines.json')
DEFAULT_SETTING = get_file_path('default.json')
ALLOWED_OPTIONS = get_file_path('allowed_options.json')