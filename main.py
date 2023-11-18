import json
import signal
import os
import argparse
from src.model.search_entry import SearchEntry
from src.model.search_driver import SearchDriver
from src.utils import paths, default
from errors.InvalidUsageError import InvalidUsageError


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--keyword", help="The keyword you want to search for", default="")
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


def command_switch():
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
            parsed_cmd['se'] = args.search_engine if args.search_engine is not None else default_options['se']
            parsed_cmd['method'] = args.type if args.type is not None else "web"
            parsed_cmd['all'] = args.all
    return parsed_cmd


def show_help_menu(error_message):
    menu = \
'''
usage: main.py [-h] [-w KEYWORD] [-s SEARCH_ENGINE] [-b BROWSER] [-t TYPE] [-a] [--change-default]
               [--display-default] [--show-functions]

options:
  -h, --help            show this help message and exit
  -w KEYWORD, --keyword KEYWORD
                        The keyword you want to search for
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
    options = command_switch()

    if not options.get("done"):
        search_entry_pool = []
        # Special case:
        # When user select option "all"
        if options.get('all'):
            search_engines_names = []
            with open(paths.ALLOWED_OPTIONS) as f:
                search_engines_json = json.load(f)['search_engines']
                if 'method' not in options.keys():
                    options['method'] = 'web'
                for k in search_engines_json:
                    # Filter out not supported search engines if the method is not supported
                    if options['method'] in k['methods']:
                        search_engines_names.append(k['name'])
                    
            for se in search_engines_names:
                options['se'] = se
                entry = SearchEntry(options)
                entry.prepare_search()
                search_entry_pool.append(entry)
        else:
            entry = SearchEntry(options)
            entry.prepare_search()
            search_entry_pool.append(entry)

        # Setup signal listeners:
        main_pid = os.getpid()
        os.fork()
        
        if os.getpid() == main_pid:
            # Wait until the SIGINT is send to main process to end the process
            search_driver = SearchDriver(search_entry_pool, options['browser'])
            search_driver.configure_browser()
            signal.signal(signal.SIGINT, lambda x, y: print("Session ended"))
            search_driver.execute_search()
            signal.pause()
            search_driver.webdriver.quit()
        else:
            user_input = input()
            if user_input.lower() == 'quit':
                os.kill(main_pid, signal.SIGINT)
            

if __name__ == '__main__':
    try:
        main()
    except InvalidUsageError as e:
        show_help_menu(str(e))
