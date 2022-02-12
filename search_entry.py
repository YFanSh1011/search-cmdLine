import json
import new_webdriver as browser
import automations.pinterest
from errors.InvalidUsageError import InvalidUsageError


def load_predefined(filepath, empty_dict):
    with open(filepath, 'r') as f:
        empty_dict = json.load(f)
        return empty_dict


class SearchEntry:
    browsers = {}
    websites = {}
    browsers = load_predefined('configs/browsers.json', browsers)
    websites = load_predefined('configs/search_engines.json', websites)

    def __init__(self, options):
        self.options = options
        self.url = ''
        self.params = {}
        self.browser = None
        self.browser_opts = None
        self.se = None
        self.se_name = None
        self.method = None
        self.support_login = False

    def configure_browser(self):
        # Convert the options to UPPER case before comparing:
        browser_string = self.options['browser'].upper()
        browser_of_choice = SearchEntry.browsers.get(browser_string)
        if browser_of_choice is None:
            raise InvalidUsageError('Invalid browser option.')
        self.browser, self.browser_opts = eval('browser.' + browser_of_choice['func-call'])

    def configure_search_engine(self):
        user_option = self.options['se'].upper()
        se_in_use = SearchEntry.websites.get(user_option)
        if se_in_use is None:
            raise InvalidUsageError('Unsupported search engine.')
        self.se = se_in_use
        self.se_name = user_option.lower()

    def configure_search_method(self):
        if self.options.get('method') is None:
            if self.se.get('only') is not None:
                self.method = self.se['only']
            else:
                self.method = 'text'
        else:
            user_method = self.options.get('method')
            if self.se.get(user_method) is None:
                raise InvalidUsageError('Unsupported functionality.')
            else:
                self.method = user_method
        self.se = self.se[self.method]
        self.url = self.se['base-url']
        self.support_login = False if self.se.get('support_login') is None else True

    def configure_search_keywords(self):
        if self.options.get('kw') is None:
            raise InvalidUsageError('Search keyword is required.')
        encoded_kws = self.options['kw'].strip().lower().replace(' ', '+')
        self.params['keyword'] = encoded_kws

    def configure_search_site(self):
        supported_params = self.se['query-params']
        if 'site' in self.options.keys():
            if supported_params.get('site') is None:
                raise InvalidUsageError('Unsupported functionality.')
            site_url = self.options['site'].strip().lower()
            self.params['site'] = site_url

    def configure_search_filetype(self):
        supported_params = self.se['query-params']
        if 'file' in self.options.keys():
            if supported_params.get('filetype') is None:
                raise InvalidUsageError('Unsupported functionality.')
            filetype = self.options['file'].strip().lower()
            self.params['filetype'] = filetype

    def configure_full_url(self):
        url_addition = ''
        query_params = self.se['query-params']

        if self.se['direct']:
            for (k, v) in self.params.items():
                url_addition += '&' + query_params[k] + '=' + v
        else:
            url_addition += query_params['keyword'] + '=' + self.params['keyword']
            for (k, v) in self.params.items():
                if k == 'keyword':
                    continue
                url_addition += '%20' + query_params[k] + '%3A' + self.params[k]
        self.url += url_addition

    def prepare_search(self):
        self.configure_browser()
        self.configure_search_engine()
        self.configure_search_method()
        self.configure_search_keywords()
        self.configure_search_site()
        self.configure_search_filetype()
        self.configure_full_url()

    def execute_search(self):
        self.prepare_search()

        if self.browser_opts is None:
            self.browser = self.browser()
        else:
            self.browser = self.browser(**self.browser_opts)
        self.browser.get(self.url)

        if self.support_login:
            user_option = input("Current search engine support login. Please enter y/Y if you want to login with the credentials stored in 'credentials' folder. Otherwise, enter anything else. ")
            login_mod = "automations." + self.se_name
            login_func = eval(login_mod + ".login")
            if user_option == "Y" or user_option == "y":
                login_func(self.browser)
