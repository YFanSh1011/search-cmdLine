import json
from errors.InvalidUsageError import InvalidUsageError
from src.utils import paths


class SearchEntry:
    
    _websites = None
    _search_engines = None

    def __init__(self, options):
        self.options: dict = options
        self.url: str = ''
        self.params: dict = {}
        self.se: dict = None
        self.se_name: str = None
        self.method: str = None

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

    def configure_search_keywords(self):
        if self.options.get('kw') is None:
            raise InvalidUsageError('Search keyword is required.')
        encoded_kws = self.options['kw'].strip().lower().replace(' ', '+')
        self.params['keyword'] = encoded_kws

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
        self.configure_full_url()
    
    def get_full_url(self):
        return self.url
    
    @staticmethod
    def get_predefined_search_engines():
        options = paths.SEARCH_ENGINES_JSON
        SearchEntry._search_engines = options
        SearchEntry._websites = [key for key in options]
        return SearchEntry._websites
    
    @staticmethod
    def prepare_all_entry_pool(options: dict) -> 'list[SearchEntry]':
        search_entry_pool = []
        search_engines_names = []
        
        # Load all available search engines in json config file
        with open(paths.ALLOWED_OPTIONS) as f:
            search_engines_json = json.load(f)['search_engines']
            
            # If user haven't specified the search method, use web search by default
            if 'method' not in options.keys():
                options['method'] = 'web'
            for k in search_engines_json:
                # Filter out not supported search engines if the method is not supported
                if options['method'] in k['methods']:
                    search_engines_names.append(k['name'])

        # For each SearchEntry object, configure their URLs       
        for se in search_engines_names:
            options['se'] = se
            entry = SearchEntry(options)
            entry.prepare_search()
            search_entry_pool.append(entry)
        return search_entry_pool
