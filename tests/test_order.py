import pytest
import allure
import time
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
    
    @allure.title("Проверка заказа самоката через верхнюю кнопку")
    @allure.description("Полный флоу заказа с проверкой успешного подтверждения")
    @pytest.mark.parametrize("order_data", TEST_DATA)
    def test_order_scooter_via_top_button(self, driver, order_data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        # Открытие главной страницы
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Нажатие на верхнюю кнопку заказа
        main_page.click_order_button_top()
        
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
    
    @allure.title("Проверка заказа самоката через нижнюю кнопку")
    @allure.description("Полный флоу заказа с нижней точки входа")
    @pytest.mark.parametrize("order_data", [TEST_DATA[0]])
    def test_order_scooter_via_bottom_button(self, driver, order_data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        # Открытие главной страницы
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Нажатие на нижнюю кнопку заказа
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
        order_page.confirm_order()
        
        # Проверка успешного создания заказа
        assert order_page.is_success_message_displayed(), "Модальное окно успеха не отображается"
    
    @allure.title("Проверка перехода на главную страницу через логотип Самоката")
    def test_scooter_logo_redirect(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Переход на страницу заказа и обратно через логотип
        main_page.click_order_button_top()
        
        # Добавляем небольшую паузу перед кликом на логотип
        time.sleep(1)
        
        main_page.click_scooter_logo()
        
        # Проверка, что вернулись на главную страницу
        assert main_page.is_main_page_displayed(), "Не удалось вернуться на главную страницу через логотип"
    
    @allure.title("Проверка перехода на Дзен через логотип Яндекса")
    def test_yandex_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Сохраняем идентификатор текущего окна
        main_window = driver.current_window_handle
        
        # Клик на логотип Яндекса
        main_page.click_yandex_logo()
        
        # Ожидание открытия нового окна
        time.sleep(3)  # Даем время для открытия нового окна
        
        # Переключение на новое окно
        all_windows = driver.window_handles
        
        if len(all_windows) > 1:
            new_window = [window for window in all_windows if window != main_window][0]
            driver.switch_to.window(new_window)
            
            # Даем время для загрузки страницы
            time.sleep(2)
            
            # Проверка, что открылась страница Яндекса или Дзена
            current_url = driver.current_url
            print(f"Открытый URL: {current_url}")
            
            # Проверяем различные возможные URL
            assert any(domain in current_url for domain in ['dzen.ru', 'yandex.ru', 'ya.ru']), \
                f"Не открылась страница Яндекса/Дзена. URL: {current_url}"
            
            # Закрываем новое окно и возвращаемся к основному
            driver.close()
            driver.switch_to.window(main_window)
        else:
            # Если новое окно не открылось, проверяем текущий URL
            current_url = driver.current_url
            print(f"Новое окно не открылось. Текущий URL: {current_url}")
            assert False, "Не открылось новое окно после клика на логотип Яндекса"