import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

BASE_URL = "http://localhost:5000"

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')  # Comment out if you want to see browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_homepage_title(driver):
    driver.get(BASE_URL)
    assert "Guestbook" in driver.title

def test_form_renders_properly(driver):
    driver.get(BASE_URL)
    assert driver.find_element(By.NAME, "name").is_displayed()
    assert driver.find_element(By.NAME, "message").is_displayed()
    assert driver.find_element(By.TAG_NAME, "button").is_displayed()

def test_submit_valid_message(driver):
    driver.get(BASE_URL)
    name = "TestUser"
    msg = "This is a test message."
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "message").send_keys(msg)
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    page = driver.page_source
    assert name in page
    assert msg in page

def test_empty_name_not_submitted(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "name").send_keys("")
    driver.find_element(By.NAME, "message").send_keys("No name provided")
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    assert "No name provided" not in driver.page_source

def test_empty_message_not_submitted(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "name").send_keys("EmptyMessageUser")
    driver.find_element(By.NAME, "message").send_keys("")
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    assert "EmptyMessageUser" not in driver.page_source

def test_submit_multiple_messages(driver):
    driver.get(BASE_URL)
    for i in range(2):
        driver.find_element(By.NAME, "name").clear()
        driver.find_element(By.NAME, "message").clear()
        driver.find_element(By.NAME, "name").send_keys(f"MultiUser{i}")
        driver.find_element(By.NAME, "message").send_keys(f"Multi message {i}")
        driver.find_element(By.TAG_NAME, "button").click()
        sleep(0.5)
    page = driver.page_source
    assert "MultiUser0" in page and "Multi message 1" in page

def test_submit_long_message(driver):
    driver.get(BASE_URL)
    long_text = "L" * 500
    driver.find_element(By.NAME, "name").send_keys("LongMsgUser")
    driver.find_element(By.NAME, "message").send_keys(long_text)
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    assert "LongMsgUser" in driver.page_source

def test_message_persists_after_refresh(driver):
    driver.get(BASE_URL)
    name = "PersistentGuy"
    message = "This message should stay after refresh"
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "message").send_keys(message)
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    driver.refresh()
    assert name in driver.page_source and message in driver.page_source

def test_redirect_after_submission(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "name").send_keys("RedirectUser")
    driver.find_element(By.NAME, "message").send_keys("Testing redirect")
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    assert driver.current_url == BASE_URL + "/"

def test_html_script_injection_sanitized(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "name").send_keys("XSSAttacker")
    driver.find_element(By.NAME, "message").send_keys("<script>alert('Hacked!')</script>")
    driver.find_element(By.TAG_NAME, "button").click()
    sleep(1)
    page = driver.page_source
    assert "<script>" not in page

