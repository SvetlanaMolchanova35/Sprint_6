import pytest
import allure
from pages.main_page import MainPage


class TestFAQ:
    
    @allure.title("Тест FAQ вопросов")
    @allure.description("Проверка отображения ответов при клике на вопросы")
    @pytest.mark.parametrize("question_index", list(range(8)))
    def test_faq_questions(self, driver, question_index):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        
        # Прокрутка до секции FAQ
        faq_section = main_page.find_element(main_page.FAQ_SECTION)
        driver.execute_script("arguments[0].scrollIntoView();", faq_section)
        
        # Ожидание загрузки FAQ
        import time
        time.sleep(1)
        
        # Клик на вопрос через JavaScript (чтобы избежать перекрытия)
        question_locator = main_page.FAQ_QUESTIONS[question_index]
        question_element = main_page.find_element(question_locator)
        
        # Прокручиваем элемент в центр экрана
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_element)
        time.sleep(0.5)
        
        # Клик через JavaScript
        driver.execute_script("arguments[0].click();", question_element)
        
        # Проверка отображения ответа
        assert main_page.is_faq_answer_displayed(question_index), \
            f"Ответ на вопрос {question_index + 1} не отображается"
        
        # Проверка, что ответ не пустой
        answer_text = main_page.get_faq_answer_text(question_index)
        assert answer_text, f"Ответ на вопрос {question_index + 1} пустой"