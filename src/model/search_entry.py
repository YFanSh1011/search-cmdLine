import json
from errors.InvalidUsageError import InvalidUsageError
from src.utils import paths


class SearchEntry:
    
    _websites = None
    _search_engines = None

    def __init__(self, options):
        self.options = options
        self.url = ''
        self.params = {}
        self.se = None
        self.se_name = None
        self.method = None
        self.support_login = False

    @staticmethod
    def get_predefined_search_engines():
        with open(paths.SEARCH_ENGINES, 'r') as f:
            options = json.load(f)
            SearchEntry._search_engines = options
            SearchEntry._websites = [key for key in options]
        return SearchEntry._websites

    def configure_search_engine(self):
        user_option = self.options['se'].upper()
        se_in_use = SearchEntry._search_engines.get(user_option)
        if se_in_use is None:
            raise InvalidUsageError('Unsupported search engine.')
        self.se = se_in_use
        self.se_name = user_option.lower()

    def configure_search_method(self):
        if self.options.get('method') is None:
            if self.se.get('only') is not None:
                self.method = self.se['only']
            else:
                self.method = 'web'
        else:
            user_method = self.options.get('method')
            if self.se.get(user_method) is None:
                raise InvalidUsageError(f'Unsupported functionality: search method {user_method} not supported in {self.se_name}')
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
                raise InvalidUsageError('Unsupported functionality: search site.')
            site_url = self.options['site'].strip().lower()
            self.params['site'] = site_url

    def configure_search_filetype(self):
        supported_params = self.se['query-params']
        if 'file' in self.options.keys():
            if supported_params.get('filetype') is None:
                raise InvalidUsageError('Unsupported functionality: file type.')
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
        self.configure_search_engine()
        self.configure_search_method()
        self.configure_search_keywords()
        self.configure_search_site()
        self.configure_search_filetype()
        self.configure_full_url()