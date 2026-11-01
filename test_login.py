import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.saucedemo.com"


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.get(URL)
    yield d
    d.quit()


def login(driver, username, password):
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def test_valid_login(driver):
    login(driver, "standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url


def test_invalid_password(driver):
    login(driver, "standard_user", "wrong_password")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "do not match" in error.text


def test_locked_out_user(driver):
    login(driver, "locked_out_user", "secret_sauce")
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "locked out" in error.text