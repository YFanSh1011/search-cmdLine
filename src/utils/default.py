import json
from errors.InvalidUsageError import InvalidUsageError
from src.model.search_command import SearchCommand
from src.model.search_entry import SearchEntry
from src.utils import paths


def display_default():
    print(paths.DEFAULT_SETTING_JSON)


def load_default():
    validate_default(paths.DEFAULT_SETTING_JSON)
    return paths.DEFAULT_SETTING_JSON


def validate_default(config):
    default_browser = config.get('browser')
    default_se_options = config.get('se')

    if default_se_options is None and default_browser is None:
        raise InvalidUsageError("Empty default.json file.")

    if default_browser is not None:
        if default_browser.upper() not in SearchCommand.get_predefined_browsers():
            raise InvalidUsageError("Invalid browser option.")
    if default_se_options is not None:
        valid_search_engines = SearchEntry.get_predefined_search_engines()
        for value in  default_se_options.values():
            if value.upper() not in valid_search_engines:
                raise InvalidUsageError("Invalid search engine option.")


def change_default(options):
    validate_default(options)
    config_json = json.dumps(options, indent=4)
    with open(paths.DEFAULT_SETTING, 'w') as f:
        f.write(config_json)

    print("Success. Current default: ")
    display_default()