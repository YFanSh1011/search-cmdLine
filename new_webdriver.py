import selenium.webdriver as webdriver

# Only return the Class instead of returning the instance
# Else the webdriver will be executed without checking the conditions
def new_chrome_driver():
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    kwargs = {"options": opts}
    return webdriver.Chrome, kwargs

def new_gecko_driver():
    return webdriver.Firefox, None