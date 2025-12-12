from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class OrderPage(BasePage):
    # Локаторы для страницы заказа
    NAME_FIELD = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME_FIELD = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_FIELD = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_FIELD = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_STATION_OPTION = (By.XPATH, "//div[@class='Order_Text__2broi']")  # Первая станция
    PHONE_FIELD = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")
    
    # Локаторы для второй страницы заказа
    DATE_FIELD = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    TODAY_DATE = (By.XPATH, "//div[contains(@class, 'react-datepicker__day--today')]")
    RENTAL_PERIOD_FIELD = (By.XPATH, "//div[text()='* Срок аренды']")
    RENTAL_PERIOD_OPTION = (By.XPATH, "//div[text()='сутки']")
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    COLOR_GREY_CHECKBOX = (By.ID, "grey")
    COMMENT_FIELD = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[@class='Button_Button__ra12g Button_Middle__1CSJM']")
    
    # Локаторы для модального окна подтверждения
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class, 'Order_Modal__')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")
    
    @allure.step("Заполнить личную информацию")
    def fill_personal_info(self, name, surname, address, phone):
        self.fill_field(self.NAME_FIELD, name)
        self.fill_field(self.SURNAME_FIELD, surname)
        self.fill_field(self.ADDRESS_FIELD, address)
        
        # Выбор станции метро
        self.click_element(self.METRO_FIELD)
        self.click_element(self.METRO_STATION_OPTION)
        
        self.fill_field(self.PHONE_FIELD, phone)
    
    @allure.step("Нажать кнопку 'Далее'")
    def click_next_button(self):
        self.click_element(self.NEXT_BUTTON)
    
    @allure.step("Заполнить информацию об аренде")
    def fill_rental_info(self, date_element_locator=None, period="сутки", color="black", comment=""):
        # Выбор даты
        self.click_element(self.DATE_FIELD)
        
        if date_element_locator:
            self.click_element(date_element_locator)
        else:
            # По умолчанию выбираем сегодняшнюю дату
            self.click_element(self.TODAY_DATE)
        
        # Выбор срока аренды
        self.click_element(self.RENTAL_PERIOD_FIELD)
        period_locator = (By.XPATH, f"//div[text()='{period}']")
        self.click_element(period_locator)
        
        # Выбор цвета
        if color == "black":
            self.click_element(self.COLOR_BLACK_CHECKBOX)
        elif color == "grey":
            self.click_element(self.COLOR_GREY_CHECKBOX)
        
        # Заполнение комментария
        if comment:
            self.fill_field(self.COMMENT_FIELD, comment)
    
    @allure.step("Нажать кнопку 'Заказать'")
    def click_order_button(self):
        self.click_element(self.ORDER_BUTTON)
    
    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.click_element(self.CONFIRM_BUTTON)
    
    @allure.step("Проверить отображение сообщения об успехе")
    def is_success_message_displayed(self):
        return self.is_element_visible(self.SUCCESS_MODAL)
    
    @allure.step("Получить текст сообщения об успехе")
    def get_success_message_text(self):
        element = self.find_element(self.SUCCESS_MESSAGE)
        return element.text