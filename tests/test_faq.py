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
        
        # Прокрутка до секции FAQ через Page Object
        main_page.scroll_to_faq_section()
        
        # Клик на вопрос через Page Object
        main_page.click_faq_question(question_index)
        
        # Проверка отображения ответа
        assert main_page.is_faq_answer_displayed(question_index), \
            f"Ответ на вопрос {question_index + 1} не отображается"
        
        # Проверка текста ответа
        actual_answer = main_page.get_faq_answer_text(question_index)
        expected_answer = main_page.FAQ_EXPECTED_ANSWERS[question_index]
        
        assert actual_answer == expected_answer, \
            f"Неверный текст ответа на вопрос {question_index + 1}\n" \
            f"Ожидалось: {expected_answer}\n" \
            f"Получено: {actual_answer}"