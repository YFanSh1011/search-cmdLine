import json
import new_webdriver as browser
from errors.InvalidUsageError import InvalidUsageError


def load_predefined(filepath, empty_dict):
    with open(filepath, 'r') as f:
        empty_dict = json.load(f)
    return empty_dict

class SearchDriver:
    browsers = {}
    browsers = load_predefined('configs/browsers.json', browsers)

    def __init__(self, search_entries, webdriver_str):
        self.search_entries = search_entries
        self.webdriver_str = webdriver_str
        self.webdriver = None

    def configure_browser(self):
        # Convert the options to UPPER case before comparing:
        browser_string = self.webdriver_str.upper()
        if (browser_string.lower() == "firefox"):
            self.webdriver = browser.new_gecko_driver()
        elif (browser_string.lower() == 'chrome'): 
            self.webdriver = browser.new_chrome_driver()

    def execute_search(self):
        if len(self.search_entries) > 1:
            for i in range(len(self.search_entries)):
                self.webdriver.switch_to.window(self.webdriver.window_handles[i])
                self.webdriver.get(self.search_entries[i].url)
                if i < len(self.search_entries) - 1:
                    self.webdriver.execute_script("window.open()")
        else:
            self.webdriver.get(self.search_entries[0].url)