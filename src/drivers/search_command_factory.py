import platform
from src.utils import paths

class SearchCommandFactory:
    @staticmethod
    def get_search_command(driver_type):
        factories = {
            "chrome": ChromeSearchCommand(),
            "firefox": FirefoxSearchCommand()
        }
        return factories[driver_type].get_command(platform.system().lower())

class ChromeSearchCommand(SearchCommandFactory):
    def get_command(self, os: str):
        browser_commands = paths.BROWSERS_JSON['chrome']
        if (os.lower() in browser_commands):
            return browser_commands[os.lower()]
        else:
            return browser_commands['default']
        

class FirefoxSearchCommand(SearchCommandFactory):
    def get_command(self, os: str):
        browser_commands = paths.BROWSERS_JSON['firefox']
        if (os.lower() in browser_commands):
            return browser_commands[os.lower()]
        else:
            return browser_commands['default']