import allure

from pages.base_page import BasePage
from playwright.sync_api import expect

from pages.profile_page import ProfilePageLocators


class MainPageLocators:
    class LocationPopUp:
        yes = "//button[text()='Да, верно']"
        no = "//button[text()='Нет, другой']"

    class AuthPopUp:
        phone = "//input[@placeholder='Номер телефона']"
        politics_auth = "//label[@class='custom-control-label']"
        get_code = "//span[text()='Получить код']"
        password = "//input[@type='tel']"
        confirm = "//span[text()='Подтвердить']"

    class SearchCity:
        search = "//input[@type='search']"
        cities_list = "//div[@class='location-modal__city']"
        close = "//button[text()='Закрыть']"

    class SubHeader:
        location = "//div[@class='location header__location']//span[@class='font-bold text-sm']"
        delivery = "//nav[@class='navbar']//a[text()='Доставка']"
        pickup = "//nav[@class='navbar']//a[text()='Пункты выдачи']"
        help = "//nav[@class='navbar']//a[text()='Помощь']"

    class Header:
        logo = "//div[@class='logo header__logo']"
        catalog = "//span[text()='Каталог']"
        catalog_list = "//li[@class='catalog-categories-navbar__item']"
        category_list = "//div[@class='catalog-categories-item']"
        search_input = "//input[@placeholder='Поиск']"
        search_button = "//span[text()='Найти']"
        orders = "//span[text()='Заказы']"
        favorites = "//span[text()='Избранное']"
        favorites_badge = "//div[@class='cart-badge-favorite font-bold text-sm']"
        basket = "//a//img[@alt='Иконка раздела корзина']"
        personal_cabinet = "//span[text()='Войти']"
        profile = "//div[@class='header__profile']"

    class Card:
        card_image_list = "//div[@class='card__image']"
        to_basket_list = "//span[text()='В корзину']"
        to_favorite_list = "//button[@aria-label='Добавить в избранное']"
        to_goods_list = "//span[text()='К товару']"
        variant_list = "//div[@class='product__content']//div[@class='product__list-item']"
        variant_to_basket_list = "//div[@class='product__content']//span[text()='В корзину']"
        variant_to_favorite_list = "//div[@class='product__content']//span[text()='В избранное']"
        article = "//div[@class='product__article text-sm font-bold']"

    class Footer:
        socials_item_list = "//div[@class='footer__socials']//a[@target='_blank']"
        apps_items_list = "//div[@class='footer__apps-items']//a"


class MainPage(BasePage):

    @allure.step("Смена локации на {change_city}")
    def change_location(self, change_city):
        self.click(locator=MainPageLocators.SubHeader.location)
        self.input_text(locator=MainPageLocators.SearchCity.search, text=change_city)
        self.click(locator=MainPageLocators.SearchCity.cities_list)

    @allure.step("Ввод пароля")
    def input_password(self, number_of_symbols, symbol):
        for index in range(number_of_symbols):
            self.page.locator(MainPageLocators.AuthPopUp.password).nth(index).fill(symbol)

    @allure.step("Авторизация пользователя {username}")
    def authorize_user(self, username):
        self.go_to()
        self.click(MainPageLocators.LocationPopUp.yes)
        self.click(MainPageLocators.Header.personal_cabinet)
        self.input_text(MainPageLocators.AuthPopUp.phone, text=username)
        self.click(MainPageLocators.AuthPopUp.politics_auth)
        self.click(MainPageLocators.AuthPopUp.get_code)
        self.input_password(number_of_symbols=4, symbol="1")
        self.click(MainPageLocators.AuthPopUp.confirm)

        expect(self.locator(ProfilePageLocators.ProfileTabs.personal_data)). \
            to_have_text("Личная информация", timeout=2000)
