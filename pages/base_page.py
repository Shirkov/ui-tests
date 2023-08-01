from datetime import datetime

import allure
from allure_commons.types import AttachmentType

from settings.env_config import settings
from start_tests import LOG


def screenshot_on_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            now = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
            filename = f"{func.__name__}_{now}.png"
            allure.attach(args[0].page.screenshot(path=filename),
                          attachment_type=AttachmentType.PNG)

            LOG.info(f"\nОшибка {e}, создан скриншот {filename}\n"
                     f'Вызываемый метод {func.__name__}, параметры args {args}')

            raise e

    return wrapper


class BasePage:
    def __init__(self, page):
        self.page = page

    def page_url(self):
        return self.page.url

    def locator(self, locator):
        return self.page.locator(locator)

    def locator_inner_text(self, locator):
        return self.page.locator(locator).inner_text()

    @allure.step("Открытие сайта")
    def go_to(self):
        return self.page.goto(settings.browser.base_url)

    @allure.step("Переход на страницу {url}")
    def go_to_url(self, url: str):
        return self.page.goto(f"{settings.browser.base_url}/{url}")

    @screenshot_on_error
    @allure.step("Клик элемента {locator}")
    def click(self, locator, index: int = 0):
        return self.page.locator(locator).nth(index).click()

    @allure.step("Выполнение скрипта {script}")
    def evaluate(self, script: str, timeout: int = 10000):
        return self.page.evaluate(script, timeout)

    @screenshot_on_error
    @allure.step("Наведение курсора на элемент {locator}")
    def hover(self, locator, index: int = 0):
        return self.page.locator(locator).nth(index).hover()

    @screenshot_on_error
    @allure.step("Ввод текста {text} в локатор {locator}")
    def input_text(self, locator, text):
        return self.page.locator(locator).fill(text)

    @screenshot_on_error
    @allure.step("Ввод текста {text} после очищения поля в локатор {locator}")
    def input_text_after_clear(self, locator, text):
        self.page.locator(locator).fill("")
        self.page.locator(locator).fill(text)

    @screenshot_on_error
    @allure.step("Клик мышкой по координатам {x}*{y}")
    def mouse_click(self, x: int, y: int):
        return self.page.mouse.click(x, y)
