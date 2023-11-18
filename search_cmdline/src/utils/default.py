import json
from search_cmdline.errors.InvalidUsageError import InvalidUsageError
from search_cmdline.src.model.search_driver import SearchDriver
from search_cmdline.src.model.search_entry import SearchEntry
from search_cmdline.src.utils import paths


def display_default():
    with open(paths.DEFAULT_SETTING, 'r') as f:
        for line in f.readlines():
            print(line)


def load_default():
    with open(paths.DEFAULT_SETTING, 'r') as f:
        default_config = json.load(f)
        validate_default(default_config)
        return default_config


def validate_default(config):
    default_browser = config.get('browser')
    default_se = config.get('se')

    if default_se is None and default_se is None:
        raise InvalidUsageError("Empty default.json file.")

    if default_browser is not None:
        if default_browser.upper() not in SearchDriver.get_predefined_browsers():
            raise InvalidUsageError("Invalid browser option.")
    if default_se is not None:
        if default_se.upper() not in SearchEntry.get_predefined_search_engines():
            raise InvalidUsageError("Invalid search engine option.")


def change_default(options):
    validate_default(options)
    config_json = json.dumps(options, indent=4)
    with open(paths.DEFAULT_SETTING, 'w') as f:
        f.write(config_json)

    print("Success. Current default: ")
    display_default()