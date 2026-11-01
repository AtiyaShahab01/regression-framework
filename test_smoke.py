from selenium import webdriver
from selenium.webdriver.common.by import By

def test_login_page_loads():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    assert driver.find_element(By.ID, "login-button").is_displayed()
    driver.quit()