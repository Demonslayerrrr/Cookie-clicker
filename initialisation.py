from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_driver():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    return driver


def setup_game(driver):
    driver.get("localhost:8000")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "langSelect-EN"))
    ).click()
    big_cookie = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "bigCookie"))
    )
    return big_cookie


def initialize():
    driver = initialize_driver()
    big_cookie = setup_game(driver)
    return driver, big_cookie
