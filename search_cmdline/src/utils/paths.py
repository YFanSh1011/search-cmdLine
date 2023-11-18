from pkg_resources import resource_filename

def get_file_path(filename):
    # Construct the full path for the JSON file
    json_path = resource_filename('search_cmdline', f'configs/{filename}')
    return json_path

# Example usage
SEARCH_ENGINES = get_file_path('search_engines.json')
DEFAULT_SETTING = get_file_path('default.json')
ALLOWED_OPTIONS = get_file_path('allowed_options.json')