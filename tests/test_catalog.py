import time

import allure

from pages.card_page import CardPage, CardPageLocators
from pages.catalog_page import CatalogPageLocator
from pages.main_page import MainPage, MainPageLocators
from playwright.sync_api import expect


@allure.epic("Тесты на каталог")
class TestCatalogPage:

    @allure.description("Выдача списка каталога и его категорий"
                        "Проверяется что список каталога не пустой и у наведенного мышкой каталога есть категории")
    def test_get_catalog_and_category_list(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Header.catalog)
        main_page.hover(MainPageLocators.Header.catalog_list, index=1)
        expect(main_page.locator(MainPageLocators.Header.catalog_list)).not_to_have_count(0)
        expect(main_page.locator(MainPageLocators.Header.category_list)).not_to_have_count(0)

    @allure.description("Переход на страницу каталога"
                        "Проверяется что список товаров каталога не пустой, "
                        "список фильтрой не пустой")
    def test_go_to_catalog_page(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Header.catalog)
        main_page.click(MainPageLocators.Header.catalog_list, index=1)
        expect(main_page.locator(CatalogPageLocator.card_list)).not_to_have_count(0, timeout=2000)
        expect(main_page.locator(CatalogPageLocator.filter_list)).not_to_have_count(0, timeout=2000)

    @allure.description("Просмотр карточки вариативного товара, переход между вариантами"
                        "Проверяется что у разных вариантов товара url и артикул отличается")
    def test_switch_between_product_variants(self, browser):
        main_page = MainPage(browser)
        main_page.go_to_url(url="catalog/aromatizatory-140000/")
        main_page.click(MainPageLocators.Card.to_goods_list)
        main_page.click(MainPageLocators.Card.variant_list)
        time.sleep(2)
        url1 = main_page.page_url()
        article1 = main_page.locator_inner_text(MainPageLocators.Card.article)
        main_page.click(MainPageLocators.Card.variant_list)
        time.sleep(2)
        url2 = main_page.page_url()
        article2 = main_page.locator_inner_text(MainPageLocators.Card.article)

        assert url1 != url2
        assert article1 != article2

    @allure.description("Открытие и закрытие фото товара."
                        "Проверяется, что активен элемент закрытия фото, "
                        "после закрытия, что кнопка 'В корзину' видимая")
    def test_open_and_close_product_photo(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.card_image_list)
        card_page = CardPage(browser)
        card_page.click(CardPageLocators.product_slider_img, index=1)
        time.sleep(2)
        expect(card_page.locator(CardPageLocators.close)).to_be_enabled(timeout=5000)
        card_page.click(CardPageLocators.close)
        expect(card_page.locator(CardPageLocators.to_basket)).to_be_visible(timeout=5000)

    @allure.description("Доступность расшаривания ссылки товара. "
                        "Проверяется, что список ссылок для рассылки не равен 0")
    def test_availability_product_share_links(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.card_image_list)
        card_page = CardPage(browser)
        card_page.click(CardPageLocators.share)
        expect(card_page.locator(CardPageLocators.share_link_list)).not_to_have_count(0)


