from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_products_displayed(logged_in):
    items = logged_in.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(items) == 6


def test_add_to_cart(logged_in):
    logged_in.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    badge = logged_in.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"


def test_remove_from_cart(logged_in):
    logged_in.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    logged_in.find_element(By.ID, "remove-sauce-labs-backpack").click()
    badges = logged_in.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0


def test_checkout(logged_in):
    wait = WebDriverWait(logged_in, 20)

    logged_in.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    logged_in.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Test")
    logged_in.find_element(By.ID, "last-name").send_keys("User")
    logged_in.find_element(By.ID, "postal-code").send_keys("12345")
    logged_in.find_element(By.ID, "continue").click()

    wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

    header = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    assert "Thank you for your order" in header.text


def test_product_images_unique(logged_in):
    images = logged_in.find_elements(By.CSS_SELECTOR, ".inventory_item_img img")
    sources = {img.get_attribute("src") for img in images}
    assert len(sources) == 6