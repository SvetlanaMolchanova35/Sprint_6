from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/"
    
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Найти элемент")
    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    @allure.step("Найти элементы")
    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}"
        )

    @allure.step("Перейти на сайт")
    def go_to_site(self):
        return self.driver.get(self.BASE_URL)

    @allure.step("Кликнуть на элемент")
    def click_element(self, locator):
        element = self.find_element(locator)
        element.click()

    @allure.step("Заполнить поле")
    def fill_field(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Ожидать видимости элемента")
    def wait_for_element_visibility(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_for_element_visibility(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Прокрутить к элементу")
    def scroll_to_element(self, locator_or_element):
        if isinstance(locator_or_element, tuple):
            element = self.find_element(locator_or_element)
        else:
            element = locator_or_element
        
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element

    @allure.step("Кликнуть через JavaScript")
    def click_element_with_js(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ожидать кликабельности элемента")
    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Получить текущее окно")
    def get_current_window_handle(self):
        return self.driver.current_window_handle

    @allure.step("Получить все окна")
    def get_window_handles(self):
        return self.driver.window_handles

    @allure.step("Переключиться на окно")
    def switch_to_window(self, window_handle):
        self.driver.switch_to.window(window_handle)

    @allure.step("Закрыть текущее окно")
    def close_current_window(self):
        self.driver.close()

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Дождаться нового окна")
    def wait_for_new_window(self, timeout=10):
        """Дождаться открытия нового окна"""
        current_windows = self.get_window_handles()
        WebDriverWait(self.driver, timeout).until(
            lambda driver: len(driver.window_handles) > len(current_windows)
        )
        return self.get_window_handles()