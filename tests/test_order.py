import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.order_page import OrderPage


class TestOrderScooter:
    
    # Тестовые данные
    TEST_DATA = [
        {
            "name": "Иван",
            "surname": "Иванов",
            "address": "ул. Ленина, д. 1",
            "phone": "+79991234567",
            "period": "сутки",
            "color": "black",
            "comment": "Позвонить за час"
        },
        {
            "name": "Мария",
            "surname": "Петрова",
            "address": "пр. Мира, д. 15",
            "phone": "+79998765432",
            "period": "трое суток",
            "color": "grey",
            "comment": "Оставить у двери"
        }
    ]
    
    @allure.title("Проверка заказа самоката")
    @allure.description("Полный флоу заказа с проверкой успешного подтверждения")
    @pytest.mark.parametrize("order_data, order_button", [
        (TEST_DATA[0], "top"),
        (TEST_DATA[1], "top"),
        (TEST_DATA[0], "bottom")
    ])
    def test_order_scooter(self, driver, order_data, order_button):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        # Открытие главной страницы
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Нажатие на кнопку заказа (верхнюю или нижнюю)
        if order_button == "top":
            main_page.click_order_button_top()
        else:
            main_page.click_order_button_bottom()
        
        # Заполнение первой страницы заказа
        order_page.fill_personal_info(
            order_data["name"],
            order_data["surname"],
            order_data["address"],
            order_data["phone"]
        )
        order_page.click_next_button()
        
        # Заполнение второй страницы заказа
        order_page.fill_rental_info(
            period=order_data["period"],
            color=order_data["color"],
            comment=order_data["comment"]
        )
        order_page.click_order_button()
        
        # Подтверждение заказа
        order_page.confirm_order()
        
        # Проверка успешного создания заказа
        assert order_page.is_success_message_displayed(), "Модальное окно успеха не отображается"
        
        success_text = order_page.get_success_message_text()
        assert "Заказ оформлен" in success_text, f"Неверное сообщение об успехе: {success_text}"
    
    @allure.title("Проверка перехода на главную страницу через логотип Самоката")
    def test_scooter_logo_redirect(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Переход на страницу заказа и обратно через логотип
        main_page.click_order_button_top()
        main_page.click_scooter_logo()
        
        # Проверка, что вернулись на главную страницу
        assert main_page.is_main_page_displayed(), "Не удалось вернуться на главную страницу через логотип"
    
    @allure.title("Проверка перехода на Дзен через логотип Яндекса")
    def test_yandex_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Сохраняем идентификатор текущего окна
        main_window = main_page.get_current_window_handle()
        
        # Получаем текущие окна до клика
        windows_before = main_page.get_window_handles()
        
        # Клик на логотип Яндекса
        main_page.click_yandex_logo()
        
        # Ожидание открытия нового окна (без time.sleep!)
        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(len(windows_before) + 1)
        )
        
        # Получаем все окна после клика
        windows_after = main_page.get_window_handles()
        
        # Находим новое окно
        new_window = [window for window in windows_after if window not in windows_before][0]
        
        # Переключаемся на новое окно
        main_page.switch_to_window(new_window)
        
        # Ожидаем загрузки страницы (не about:blank)
        WebDriverWait(driver, 10).until(
            lambda d: d.current_url not in ['about:blank', '']
        )
        
        # Проверяем URL
        current_url = main_page.get_current_url()
        assert any(domain in current_url for domain in ['dzen.ru', 'yandex.ru', 'ya.ru']), \
            f"Не открылась страница Яндекса/Дзена. URL: {current_url}"
        
        # Закрываем новое окно и возвращаемся к основному
        main_page.close_current_window()
        main_page.switch_to_window(main_window)