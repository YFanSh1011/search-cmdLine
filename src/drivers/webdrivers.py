import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


def new_chrome_driver():
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    return driver

def new_gecko_driver():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    return driver