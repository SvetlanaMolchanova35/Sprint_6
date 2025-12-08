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
    
    # Кнопка принятия куки (если есть)
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")
    
    def accept_cookies(self):
        if self.is_element_visible(self.COOKIE_BUTTON):
            self.click_element(self.COOKIE_BUTTON)
    
    def click_faq_question(self, question_index):
        question_locator = self.FAQ_QUESTIONS[question_index]
        question_element = self.find_element(question_locator)
        
        # Прокручиваем элемент в центр экрана
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_element)
        
        # Клик через JavaScript для надежности
        self.driver.execute_script("arguments[0].click();", question_element)
    
    def get_faq_answer_text(self, answer_index):
        answer_locator = self.FAQ_ANSWERS[answer_index]
        answer_element = self.find_element(answer_locator)
        return answer_element.text
    
    def is_faq_answer_displayed(self, answer_index):
        answer_locator = self.FAQ_ANSWERS[answer_index]
        return self.is_element_visible(answer_locator)
    
    def click_order_button_top(self):
        self.click_element(self.ORDER_BUTTON_TOP)
    
    def click_order_button_bottom(self):
        # Прокрутка к нижней кнопке
        button = self.find_element(self.ORDER_BUTTON_BOTTOM)
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        
        # Небольшая пауза для стабилизации
        import time
        time.sleep(0.5)
        
        # Клик через JavaScript для надежности
        self.driver.execute_script("arguments[0].click();", button)
    
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)
    
    def click_yandex_logo(self):
        # Клик через JavaScript для надежности
        yandex_logo_element = self.find_element(self.YANDEX_LOGO)
        self.driver.execute_script("arguments[0].click();", yandex_logo_element)
    
    def is_main_page_displayed(self):
        return self.is_element_visible(self.ORDER_BUTTON_TOP)