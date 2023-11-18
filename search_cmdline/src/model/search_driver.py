import json
from errors.InvalidUsageError import InvalidUsageError
from src.drivers.driver_factory import WebDriverFactory
from src.utils import paths


class SearchDriver:

    _browsers = []

    def __init__(self, search_entries, browser_name):
        self.search_entries = search_entries
        self.browser_name = browser_name
        self.webdriver = None

    @staticmethod
    def get_predefined_browsers():
        with open(paths.ALLOWED_OPTIONS, 'r') as f:
            dest = [entry for entry in json.load(f)['browsers']]
        SearchDriver._browsers = dest
        return SearchDriver._browsers

    def configure_browser(self):
        # Convert the options to UPPER case before comparing:
        self.webdriver = WebDriverFactory.get_driver(self.browser_name.lower())

    def execute_search(self):
        # The situation where user selected to search in "ALL"
        if len(self.search_entries) > 1:
            for i in range(len(self.search_entries)):
                self.webdriver.switch_to.window(self.webdriver.window_handles[i])
                self.webdriver.get(self.search_entries[i].url)
                if i < len(self.search_entries) - 1:
                    self.webdriver.execute_script("window.open()")
        else:
            # The situation where user only search in one search engine
            self.webdriver.get(self.search_entries[0].url)