import os
import json

def get_file_path(filename):
    # If being launched without packaging, use direct path
    _working_dir = os.getcwd()
    return os.path.join(_working_dir, "configs", filename)

def load_file_json(filename):
    with open(get_file_path(filename)) as f:
        return json.load(f)

SEARCH_ENGINES = get_file_path('search_engines.json')
DEFAULT_SETTING = get_file_path('default.json')
ALLOWED_OPTIONS = get_file_path('allowed_options.json')
BROWSERS = get_file_path('browsers.json')

SEARCH_ENGINES_JSON: dict = load_file_json("search_engines.json")
DEFAULT_SETTING_JSON: dict = load_file_json('default.json')
ALLOWED_OPTIONS_JSON: dict = load_file_json('allowed_options.json')
BROWSERS_JSON: dict = load_file_json('browsers.json')
