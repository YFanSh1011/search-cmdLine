import sys
import json
from search_entry import SearchEntry as Search
from errors.InvalidUsageError import InvalidUsageError


def display_default():
    with open('configs/default.json', 'r') as f:
        for line in f.readlines():
            print(line)


def validate_default(config):
    default_browser = config.get('browser')
    default_se = config.get('se')

    if default_se is None and default_se is None:
        raise InvalidUsageError("Empty default.json file.")

    if default_browser is not None:
        if default_browser.upper() not in Search.browsers.keys():
            raise InvalidUsageError("Invalid browser option.")
    if default_se is not None:
        if default_se.upper() not in Search.websites.keys():
            raise InvalidUsageError("Invalid search engine option.")


def load_default():
    with open('configs/default.json', 'r') as f:
        default_config = json.load(f)
        validate_default(default_config)
        return default_config


def change_default(options):
    validate_default(options)
    config_json = json.dumps(options, indent=4)
    with open('configs/default.json', 'w') as f:
        f.write(config_json)

    print("Success. Current default: ")
    display_default()


def show_functions():
    options = {}
    with open('configs/allowed_options.json', 'r') as f:
        options = json.load(f)

    print()
    print("Supported Browsers:")
    print(options['browsers'])
    print()
    print("Supported Search Engines and Methods:")
    for se in options['search_engines']:
        print(se['name'] + ' : ' + str(se['methods']))
    print()


def command_switch(cmd):
    is_change_mode = False

    if '--set-default' in cmd:
        if len(sys.argv) == 2:
            raise InvalidUsageError("Specific default values are not specified.")
        if len(sys.argv) % 2 != 0:
            raise InvalidUsageError("Invalid number of arguments")
        is_change_mode = True

    else:
        # Check if the number command line arguments are invalid
        if len(cmd) % 2 == 0 or len(cmd) == 1:
            if len(cmd) == 2:
                if cmd[1] == '-h':
                    raise InvalidUsageError('HELP_MENU')
                elif cmd[1] == '--show-default':
                    print('Displaying the default setting:')
                    display_default()
                    raise InvalidUsageError(None)
                elif cmd[1] == '--show-functions':
                    show_functions()
                    raise InvalidUsageError(None)
                else:
                    raise InvalidUsageError("Invalid number of arguments")
        else:
            is_change_mode = False

    return is_change_mode


def parse_command(cmd, is_change_default):
    # Parse the arguments:
    # search -w chrome -o google -kw "how to write prompt"
    mapped_options = {'-w': 'browser', '-o': 'se', '-kw': 'kw', '-s': 'site', '-f': 'file', '-m': 'method'}
    parsed_cmd = {}

    if not is_change_default:
        parsed_cmd = load_default()

    for i in range(2 if is_change_default else 1, len(cmd), 2):
        corresponding_key = mapped_options[cmd[i]]
        parsed_cmd[corresponding_key] = cmd[i + 1]

    return parsed_cmd


def show_help_menu(error_message):
    menu = \
        '''
Please refer to the flags and available options:

-w [browser]        :   chrome, firefox
-o [search engine]  :   google, duckduckgo, baidu, bing, youtube, bilibili, 
-kw                 :   Arbitrary search keywords. Please enclose it with double quotes if the keyword is consisted of multiple words
-f                  :   Arbitrary file type 
                        !!!Some file types may not be applicable for certain search engine.
-s                  :   Specific domain that you would like to search in.
-m                  :   Method of search, used to specify the type of results you want [ text(default), video, image ]
                        !!! Some search methods may not be applicable for certain search engines
-h                  :   Display help menu. YUP, you are looking at it right now.


--set-default [flags]:
This flag should be the first flag following 'search'. It is used to write new config to the 'default.json' file.

--show-default:
This flag enables the program to display your current 'default.json' file.

--show-functions:
This flag is used to display all available options of browsers, search engines, and the search methods they support 
    '''
    if error_message == 'None':
        pass
    else:
        if error_message != 'HELP_MENU':
            print('Error: ' + error_message)
        print(menu)


def main():
    is_change_mode = command_switch(sys.argv)
    options = parse_command(sys.argv, is_change_mode)

    if is_change_mode:
        change_default(options)
    else:
        entry = Search(options)
        entry.execute_search()


if __name__ == '__main__':
    try:
        main()
    except InvalidUsageError as e:
        show_help_menu(str(e))
