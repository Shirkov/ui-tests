import time

import allure
import pytest
from playwright.sync_api import expect

from pages.basket_page import BasketPage, BasketPageLocators
from pages.card_page import CardPage, CardPageLocators
from pages.catalog_page import CatalogPage, CatalogPageLocator
from pages.main_page import MainPage, MainPageLocators
from pages.profile_page import ProfilePage, ProfilePageLocators


@allure.epic("Тесты на страницу избранного")
class TestFavoritePage:

    @allure.description("Добавление товара в избранное с главной страницы. "
                        "Проверяется количество товара в избранном и бейдж избранного")
    def test_add_favorite_via_main_page(self, cart_clear, favorite_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_favorite_list, index=0)
        main_page.click(MainPageLocators.Header.favorites)
        profile_page = ProfilePage(browser)
        expect(profile_page.locator(ProfilePageLocators.Favorite.card_list)).to_have_count(1, timeout=2000)
        expect(profile_page.locator(MainPageLocators.Header.favorites_badge)).to_have_text("1")

    @allure.description("Добавление товара в избранное из каталога. "
                        "Проверяется количество товара в избранном и бейдж избранного")
    def test_add_favorite_from_catalog(self, cart_clear, favorite_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to_url(url="catalog/aromatizatory-140000/")
        time.sleep(1)
        catalog_page = CatalogPage(browser)
        catalog_page.click(CatalogPageLocator.favorites_list, index=0)
        main_page.click(MainPageLocators.Header.favorites)
        profile_page = ProfilePage(browser)
        expect(profile_page.locator(ProfilePageLocators.Favorite.card_list)).to_have_count(1, timeout=2000)
        expect(profile_page.locator(MainPageLocators.Header.favorites_badge)).to_have_text("1")

    @allure.description("Добавление товара в избранное через корзину. "
                        "Проверяется количество товара в избранном и бейдж избранного")
    def test_add_to_favorites_via_basket_page(self, cart_clear, favorite_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_basket_list, index=1)
        time.sleep(1)
        main_page.click(MainPageLocators.Header.basket)
        basket_page = BasketPage(browser)
        basket_page.click(BasketPageLocators.Card.to_favorite_list, index=0)
        basket_page.click(MainPageLocators.Header.favorites)
        profile_page = ProfilePage(browser)
        expect(profile_page.locator(ProfilePageLocators.Favorite.card_list)).to_have_count(1, timeout=2000)
        expect(profile_page.locator(MainPageLocators.Header.favorites_badge)).to_have_text("1")

    @allure.description("Добавление товара в избранное через карточку товара. "
                        "Проверяется количество товара в избранном и бейдж избранного")
    def test_add_to_favorites_from_card(self, cart_clear, favorite_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to_url(url="catalog/aromatizatory-140000/")
        catalog_page = CatalogPage(browser)
        catalog_page.click(CatalogPageLocator.card_list)
        card_page = CardPage(browser)
        card_page.click(CardPageLocators.to_favorite_list)
        card_page.click(MainPageLocators.Header.favorites)
        profile_page = ProfilePage(browser)
        expect(profile_page.locator(ProfilePageLocators.Favorite.card_list)).to_have_count(1, timeout=2000)
        expect(profile_page.locator(MainPageLocators.Header.favorites_badge)).to_have_text("1")

    @allure.description("Удаление товара из избранного. "
                        "Проверяется отсутствие списка товаров в избранном и текст, что любимых товаров нет")
    def test_delete_favorite(self, cart_clear, favorite_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_favorite_list, index=0)
        main_page.click(MainPageLocators.Header.favorites)
        profile_page = ProfilePage(browser)
        profile_page.click(ProfilePageLocators.Favorite.to_favorite_list, index=0)
        expect(profile_page.locator(ProfilePageLocators.Favorite.card_list)).not_to_have_class(["card"],
                                                                                               timeout=2000)
        expect(profile_page.locator(ProfilePageLocators.Favorite.empty_block)).to_have_text(
            "Вы еще ничего не добавили в избранное", timeout=2000)
