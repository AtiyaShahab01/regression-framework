from selenium.webdriver.common.by import By


def test_login_page_loads(driver):
    assert driver.find_element(By.ID, "login-button").is_displayed()