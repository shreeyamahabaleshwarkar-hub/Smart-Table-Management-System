import subprocess
import sys
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_home_page_opens(browser):
    browser.get("http://127.0.0.1:5000")

    assert "Welcome" in browser.title
    assert browser.find_element(By.ID, "new-order").is_displayed()
    assert browser.find_element(By.ID, "help-option").is_displayed()
    assert browser.find_element(By.ID, "bill-option").is_displayed()


def test_menu_opens(browser):
    browser.get("http://127.0.0.1:5000")

    browser.find_element(By.ID, "new-order").click()

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "order-form"))
    )

    assert "Paneer Tikka" in browser.page_source


def test_quantity_and_cart_total(browser):
    browser.get("http://127.0.0.1:5000/menu")

    quantity = browser.find_element(By.ID, "quantity-2")
    quantity.clear()
    quantity.send_keys("2")

    WebDriverWait(browser, 5).until(
        lambda driver: driver.find_element(
            By.ID, "cart-total"
        ).text == "360.00"
    )

    assert browser.find_element(By.ID, "item-count").text == "2"


def test_order_confirmation(browser):
    browser.get("http://127.0.0.1:5000/menu")

    quantity = browser.find_element(By.ID, "quantity-2")
    quantity.clear()
    quantity.send_keys("2")

    browser.find_element(By.ID, "quantity-6").send_keys("1")

    browser.find_element(By.ID, "place-order").click()

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "order-reference")
        )
    )

    assert "ORDER CONFIRMED" in browser.page_source
    assert browser.find_element(By.ID, "order-reference").text
    assert "₹400.00" in browser.page_source
    