import time
from playwright.sync_api import sync_playwright, Page
from translate import Translator
from typing import List

class TwoGisMapParse:
    def __init__(self, keyword: str, sity: str):
        self.keyword = keyword  #  Ищем по ключевому слову
        self.sity = sity  # Ищем в определённом городе
        self.list_organizations_name = []  # Список для организаций

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)  # headless=False - без графического итерфейса
            self.context = browser.new_context()  # По типу вкладок инкогнито
            self.page = self.context.new_page()  # Новая страница, создается в контексте
            self.page.goto(f"https://2gis.ru/{self.translate_text(self.sity).lower()}")  #  Переходим по адресу, переводим город
            # Ищем поле поиска, пишем туда keyword и печатаем каждую букву с промежутком 0.4, нажимаем Enter
            self.page.get_by_placeholder("Поиск в 2ГИС").type(text=self.keyword, delay=0.4)
            self.page.keyboard.press('Enter')
            self.page.click('[style="transform: rotate(-90deg);"]')  # Кликаем на кнопку перехода на след. страницу
            time.sleep(2)

    def translate_text(self, text, from_lang='ru', to_lang='en'):
        # Создаем объект Translator, указывая исходный язык и язык перевода
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        try:
            # Пытаемся перевести текст
            translated_text = translator.translate(text)
            return translated_text  # Возвращаем переведенный текст
        except Exception as e:
            # Если возникает ошибка, возвращаем сообщение об ошибке
            return f"Error: {e}"

if __name__ == "__main__":
    TwoGisMapParse("Мойка", "Самара").parse()
