import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_element_by_xpath_with_wait(webdriver, xpath):
    element = WebDriverWait(webdriver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return element


def login(webdriver):
    credentials = {}
    with open('./credentials/pinterest.json', 'r') as f:
        credentials = json.load(f)

    wait = WebDriverWait(webdriver, 5)

    login_btn = find_element_by_xpath_with_wait(webdriver, "//div[contains(@data-test-id, 'login')]/button")
    login_btn.click()

    # Possibly wait for a few seconds
    email_input = find_element_by_xpath_with_wait(webdriver, "//input[@id='email']")
    password_input = find_element_by_xpath_with_wait(webdriver, "//input[@id='password']")
    submit_btn = find_element_by_xpath_with_wait(webdriver, "//button[@type='submit'][contains(@class, 'active')]")

    email_input.send_keys(credentials['email'])
    password_input.send_keys(credentials['password'])
    submit_btn.click()
