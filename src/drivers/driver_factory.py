import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager



class WebDriverFactory:
    @staticmethod
    def get_driver(driver_type):
        factories = {
            "chrome": ChromeDriverFactory(),
            "firefox": GeckoDriverFactory()
        }
        return factories[driver_type].create_driver()

class ChromeDriverFactory(WebDriverFactory):
    def create_driver(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        return driver

class GeckoDriverFactory(WebDriverFactory):
    def create_driver(self):
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        return driver