import json
import argparse
import sys
from src.model.search_entry import SearchEntry
from src.model.search_command import SearchCommand
from src.utils import paths, default
from errors.InvalidUsageError import InvalidUsageError



def parse_arguments():
    # Check sys.argv to see if any flag is present that should negate the need for 'keyword'
    conditional = any(flag in sys.argv for flag in ["--change-default", "--display-default", "--show-functions"])

    parser = argparse.ArgumentParser()

    if conditional:
        # Make keyword optional if a certain condition is met
        parser.add_argument("--keyword", help="The keyword you want to search for", default=None)
    else:
        # Keep keyword as positional argument
        parser.add_argument("keyword", help="The keyword you want to search for")

    parser.add_argument("-s", "--search-engine", help="Your preferred search engine for search")
    parser.add_argument("-b", "--browser", help="Your preferred browser to search")
    parser.add_argument("-t", "--type", help="The media type that your would like to search for: web, image, video")
    parser.add_argument("-a", "--all", help="Flag to indicate that you want to search on all compatible search engines",
                        action="store_true")
    parser.add_argument("--change-default", help="Flag to indicate that you want to edit the default config file", \
                        action="store_true")
    parser.add_argument('--display-default', help="Flag to indicate that you want to review the default config", \
                        action="store_true")
    parser.add_argument("--show-functions", help="Flag to display all compatible seatch engines & their options", \
                        action="store_true")
    return parser.parse_args()
    


def show_functions():
    options = {}
    with open(paths.ALLOWED_OPTIONS, 'r') as f:
        options = json.load(f)

    print()
    print("Supported Browsers:")
    print(options['browsers'])
    print()
    print("Supported Search Engines and Methods:")
    for se in options['search_engines']:
        print(se['name'] + ' : ' + str(se['methods']))
    print()


def parse_command():
    args = parse_arguments()
    parsed_cmd = {}

    if args.change_default:
        new_config = {}
        if args.browser is not None:
            new_config['browser'] = args.browser
        if args.search_engine is not None:
            new_config['se'] = args.search_engine
        default.change_default(new_config)
        parsed_cmd['done'] = True
    elif args.display_default:
        default.display_default()
        parsed_cmd['done'] = True
    elif args.show_functions:
        show_functions()
        parsed_cmd['done'] = True
    else:
        if not args.keyword:
            raise InvalidUsageError("search keyword not specified")
        else:
            default_options = default.load_default()
            parsed_cmd['kw'] = args.keyword
            parsed_cmd['browser'] = args.browser if args.browser is not None else default_options['browser']
            search_method = args.type if args.type is not None else "web"
            parsed_cmd['method'] = search_method
            parsed_cmd['se'] = args.search_engine if args.search_engine is not None else default_options['se'].get(search_method)
            parsed_cmd['all'] = args.all
    return parsed_cmd


def show_help_menu(error_message):
    menu = \
'''
usage: main.py [-h] [-s SEARCH_ENGINE] [-b BROWSER] [-t TYPE] [-a] [--change-default] [--display-default] [--show-functions] keyword

positional arguments:
  keyword               The keyword you want to search for

options:
  -h, --help            show this help message and exit
  -s SEARCH_ENGINE, --search-engine SEARCH_ENGINE
                        Your preferred search engine for search
  -b BROWSER, --browser BROWSER
                        Your preferred browser to search
  -t TYPE, --type TYPE  The media type that your would like to search for: web, image, video
  -a, --all             Flag to indicate that you want to search on all compatible search engines
  --change-default      Flag to indicate that you want to edit the default config file
  --display-default     Flag to indicate that you want to review the default config
  --show-functions      Flag to display all compatible seatch engines & their options
'''
    if error_message == 'None':
        pass
    else:
        if error_message != 'HELP_MENU':
            print('Error: ' + error_message)
        print(menu)


def main():
    try:
        options = parse_command()

        if not options.get("done"):
            search_entry_pool = []
            # Special case:
            # When user select option "all"
            if options.get('all'):
                search_entry_pool = SearchEntry.prepare_all_entry_pool(options)
            else:
                entry = SearchEntry(options)
                entry.prepare_search()
                search_entry_pool.append(entry)
            
            search_browser = SearchCommand(search_entry_pool, options['browser'])
            search_browser.execute_search()
    except InvalidUsageError as e:
        show_help_menu(str(e))


if __name__ == '__main__':
    main()