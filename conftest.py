import os
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com"
USERNAME = os.getenv("SAUCE_USER", "standard_user")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--incognito")
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
    d = webdriver.Chrome(options=options)
    d.get(URL)
    yield d
    d.quit()


@pytest.fixture
def logged_in(driver):
    driver.find_element(By.ID, "user-name").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".inventory_item_img img")) == 6
    )
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(driver.get_screenshot_as_base64()))
            report.extras = extras