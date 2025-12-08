import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import allure
from allure_commons.types import AttachmentType


@pytest.fixture(scope="function")
def driver():
    # Настройка Firefox
    firefox_options = Options()
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    
    # Инициализация драйвера
    driver = webdriver.Firefox(options=firefox_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Закрытие драйвера после теста
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=AttachmentType.PNG
            )