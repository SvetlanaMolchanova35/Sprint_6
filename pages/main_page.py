from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    # Локаторы для FAQ
    FAQ_SECTION = (By.XPATH, "//div[contains(text(), 'Вопросы о важном')]")
    FAQ_QUESTIONS = [
        (By.ID, "accordion__heading-0"),
        (By.ID, "accordion__heading-1"),
        (By.ID, "accordion__heading-2"),
        (By.ID, "accordion__heading-3"),
        (By.ID, "accordion__heading-4"),
        (By.ID, "accordion__heading-5"),
        (By.ID, "accordion__heading-6"),
        (By.ID, "accordion__heading-7")
    ]
    
    FAQ_ANSWERS = [
        (By.ID, "accordion__panel-0"),
        (By.ID, "accordion__panel-1"),
        (By.ID, "accordion__panel-2"),
        (By.ID, "accordion__panel-3"),
        (By.ID, "accordion__panel-4"),
        (By.ID, "accordion__panel-5"),
        (By.ID, "accordion__panel-6"),
        (By.ID, "accordion__panel-7")
    ]
    
    # Локаторы для кнопок заказа
    ORDER_BUTTON_TOP = (By.XPATH, "//button[@class='Button_Button__ra12g']")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "(//button[text()='Заказать'])[2]")
    
    # Локаторы для логотипов
    SCOOTER_LOGO = (By.XPATH, "//a[@class='Header_LogoScooter__3lsAR']")
    YANDEX_LOGO = (By.XPATH, "//a[@class='Header_LogoYandex__3TSOI']")
    
    # Кнопка принятия куки
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    
    # Ожидаемые тексты ответов FAQ
    FAQ_EXPECTED_ANSWERS = [
        "Сутки — 400 рублей. Оплата курьеру — наличными или картой.",
        "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим.",
        "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.",
        "Только начиная с завтрашнего дня. Но скоро станем расторопнее.",
        "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.",
        "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится.",
        "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.",
        "Да, обязательно. Всем самокатов! И Москве, и Московской области."
    ]
    
    def accept_cookies(self):
        if self.is_element_visible(self.COOKIE_BUTTON):
            self.click_element(self.COOKIE_BUTTON)
    
    def click_faq_question(self, question_index):
        question_locator = self.FAQ_QUESTIONS[question_index]
        self.wait_for_element_to_be_clickable(question_locator)
        self.click_element_with_js(question_locator)
    
    def get_faq_answer_text(self, answer_index):
        answer_locator = self.FAQ_ANSWERS[answer_index]
        answer_element = self.find_element(answer_locator)
        return answer_element.text
    
    def is_faq_answer_displayed(self, answer_index):
        answer_locator = self.FAQ_ANSWERS[answer_index]
        return self.is_element_visible(answer_locator)
    
    def click_order_button_top(self):
        self.wait_for_element_to_be_clickable(self.ORDER_BUTTON_TOP)
        self.click_element(self.ORDER_BUTTON_TOP)
    
    def click_order_button_bottom(self):
        # Прокрутка и клик с ожиданием кликабельности
        button = self.scroll_to_element(self.ORDER_BUTTON_BOTTOM)
        self.wait_for_element_to_be_clickable(self.ORDER_BUTTON_BOTTOM)
        self.click_element_with_js(self.ORDER_BUTTON_BOTTOM)
    
    def click_scooter_logo(self):
        self.wait_for_element_to_be_clickable(self.SCOOTER_LOGO)
        self.click_element(self.SCOOTER_LOGO)
    
    def click_yandex_logo_and_wait_for_new_window(self, current_window_handle):
        """Клик на логотип Яндекса с ожиданием нового окна"""
        self.wait_for_element_to_be_clickable(self.YANDEX_LOGO)
        self.click_element_with_js(self.YANDEX_LOGO)
        return self.switch_to_new_window(current_window_handle)
    
    def is_main_page_displayed(self):
        return self.is_element_visible(self.ORDER_BUTTON_TOP)
    
    def scroll_to_faq_section(self):
        """Прокрутка к секции FAQ"""
        return self.scroll_to_element(self.FAQ_SECTION)
    
    def check_yandex_redirect_url(self):
        """Проверка URL после перехода на Яндекс/Дзен с ожиданием загрузки"""
        # Ждем, что URL содержит один из доменов Яндекса
        for domain in ['dzen.ru', 'yandex.ru', 'ya.ru']:
            if self.wait_for_url_contains(domain, timeout=5):
                return True
        
        # Если ни один домен не найден, проверяем текущий URL
        current_url = self.get_current_url()
        return any(domain in current_url for domain in ['dzen.ru', 'yandex.ru', 'ya.ru'])