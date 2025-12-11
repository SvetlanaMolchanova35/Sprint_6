from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/"
    
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}"
        )

    def go_to_site(self):
        return self.driver.get(self.BASE_URL)

    def click_element(self, locator):
        element = self.wait_for_element_to_be_clickable(locator)
        element.click()

    def fill_field(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def wait_for_element_visibility(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_for_element_visibility(locator, timeout)
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator_or_element):
        """Прокрутка к элементу"""
        if isinstance(locator_or_element, tuple):
            element = self.find_element(locator_or_element)
        else:
            element = locator_or_element
        
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element

    def click_element_with_js(self, locator):
        """Клик через JavaScript"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        """Ожидание кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def wait_for_new_window(self, current_windows, timeout=10):
        """Ожидание открытия нового окна"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: len(driver.window_handles) > len(current_windows)
        )
    
    def switch_to_new_window(self, current_window_handle):
        """Переключение на новое окно"""
        # Ждем открытия нового окна
        self.wait_for_new_window([current_window_handle])
        
        # Находим новое окно
        all_windows = self.driver.window_handles
        new_window = [window for window in all_windows if window != current_window_handle][0]
        
        # Переключаемся
        self.driver.switch_to.window(new_window)
        return new_window
    
    def close_current_window_and_switch_to(self, window_handle):
        """Закрытие текущего окна и переключение на указанное"""
        self.driver.close()
        self.driver.switch_to.window(window_handle)
    
    def wait_for_url_contains(self, text, timeout=10):
        """Ожидание, что URL содержит определенный текст"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
            return True
        except TimeoutException:
            return False
    
    def get_current_url(self):
        """Получение текущего URL"""
        return self.driver.current_url