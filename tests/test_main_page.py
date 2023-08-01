import time

import allure
from playwright.sync_api import expect

from pages.catalog_page import CatalogPage, CatalogPageLocator
from pages.main_page import MainPage, MainPageLocators

from pages.profile_page import ProfilePage, ProfilePageLocators


@allure.epic("Тесты на главную страницу")
class TestMainPage:
    @allure.description("Авторизация пользователя по номеру телефона")
    def test_authorization(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Header.profile)
        profile_page = ProfilePage(browser)
        expect(profile_page.locator(ProfilePageLocators.ProfileTabs.personal_data)). \
            to_have_text("Личная информация", timeout=2000)

    @allure.description("Смена локации")
    def test_change_location(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.change_location(change_city="Санкт-Петербург")
        expect(main_page.locator(MainPageLocators.SubHeader.location)).to_have_text("Санкт-Петербург", timeout=5000)

    @allure.description("Выдача списка городов при изменении локации")
    def test_get_city_list_when_change_location(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(locator=MainPageLocators.SubHeader.location)
        main_page.input_text(locator=MainPageLocators.SearchCity.search, text="Влад")
        expect(main_page.locator(MainPageLocators.SearchCity.cities_list)).not_to_have_count(0, timeout=2000)

    @allure.description("Поиск товара на сайте через строку поиска."
                        "Проверяется отображение товара на странице, "
                        "часть введеного текста должна быть в названии товара")
    def test_search_goods_in_search_bar(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.input_text(MainPageLocators.Header.search_input, text="кастрюля")
        main_page.click(MainPageLocators.Header.search_button)
        catalog_page = CatalogPage(browser)
        expect(catalog_page.locator(CatalogPageLocator.card_list)).not_to_have_count(0)
        expect(catalog_page.locator(CatalogPageLocator.card_link_list)).to_contain_text(["кастрюля"], ignore_case=True)
