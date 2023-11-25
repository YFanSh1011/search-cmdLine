import subprocess
from src.model.search_entry import SearchEntry
from src.drivers.search_command_factory import SearchCommandFactory
from src.utils import paths


class SearchCommand:

    _browsers = []

    def __init__(self, search_entries, browser_name):
        self.search_entries: list[SearchEntry] = search_entries
        self.browser_name: str = browser_name
        self.search_command: list[str] = None

    @staticmethod
    def get_predefined_browsers():
        dest = [entry for entry in paths.ALLOWED_OPTIONS_JSON['browsers']]
        SearchCommand._browsers = dest
        return SearchCommand._browsers

    def configure_browser(self):
        self.search_command = SearchCommandFactory.get_search_command(self.browser_name.lower())

    def execute_search(self):
        self.configure_browser()
        # The situation where user selected to search in "ALL"
        for entry in self.search_entries:
            self.search_command.append(entry.get_full_url())
        subprocess.run(self.search_command)