import time

import allure
import pytest

from cms.cart_services import Cart
from helpers.initial_data import DeliveryMethod, InitialData, Items
from pages.basket_page import BasketPageLocators, BasketPage
from pages.main_page import MainPage, MainPageLocators
from playwright.sync_api import expect

from pages.profile_page import ProfilePage, ProfilePageLocators


@allure.epic("Тесты на корзину")
class TestBasketPage:

    @allure.description("Добавление товара в корзину в количестве 2 шт."
                        "Проверяется список и количество товаров в корзине.")
    def test_add_product_to_basket(self, cart_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_basket_list, index=1)
        time.sleep(1)
        main_page.click(MainPageLocators.Header.basket)
        basket_page = BasketPage(browser)
        basket_page.click(BasketPageLocators.Card.plus_list, index=0)
        expect(basket_page.locator(BasketPageLocators.Card.card_list)).to_have_count(1)
        expect(basket_page.locator(BasketPageLocators.Card.count_list).nth(0)).to_have_text("2")

    @allure.description("Добавление вариативного товара в корзину в количестве 2 шт."
                        "Проверяется список и количество товаров в корзине.")
    def test_add_variant_product_to_basket(self, cart_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to_url(url="catalog/aromatizatory-140000/")
        main_page.click(MainPageLocators.Card.to_goods_list)
        main_page.click(MainPageLocators.Card.variant_to_basket_list)
        time.sleep(1)
        main_page.click(MainPageLocators.Header.basket)
        basket_page = BasketPage(browser)
        basket_page.click(BasketPageLocators.Card.plus_list, index=0)
        expect(basket_page.locator(BasketPageLocators.Card.card_list)).to_have_count(1)
        expect(basket_page.locator(BasketPageLocators.Card.count_list).nth(0)).to_have_text("2")

    @allure.description("Удаление товара из корзины."
                        "Проверяется алерт, что товаров нет в корзине.")
    def test_delete_product_from_basket(self, cart_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_basket_list, index=1)
        time.sleep(1)
        basket_page = BasketPage(browser)
        basket_page.go_to_basket_checked_all()
        basket_page.click(BasketPageLocators.Card.delete_list, index=0)
        expect(basket_page.locator(BasketPageLocators.Card.empty_basket_alert)).to_have_text(
            "Упс!")

    @allure.description("Удаление всех товаров из корзины."
                        "Проверяется алерт, что товаров нет в корзине после нажатия на кнопку 'Удалить все'. ")
    def test_delete_all_product_from_basket(self, cart_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_basket_list, index=1)
        main_page.click(MainPageLocators.Card.to_basket_list, index=2)
        time.sleep(1)
        main_page.click(MainPageLocators.Header.basket)
        basket_page = BasketPage(browser)
        basket_page.click(BasketPageLocators.Card.delete_all)
        expect(basket_page.locator(BasketPageLocators.Card.empty_basket_alert)).to_have_text(
            "Упс!", timeout=10000)

    @allure.description("Расчет стоимости корзины."
                        "Сверяется сумма товарных позиций и поле 'Итого'")
    def test_basket_cost_calculation(self, cart_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Card.to_basket_list, index=1)
        main_page.click(MainPageLocators.Card.to_basket_list, index=2)
        time.sleep(1)
        main_page.click(MainPageLocators.Header.basket)
        basket_page = BasketPage(browser)

        time.sleep(3)
        sum_basket = basket_page.sum_price(basket_page.locator(BasketPageLocators.AsideColumn.total))
        sum_price_goods = basket_page.sum_price(basket_page.locator(BasketPageLocators.Card.price_list))

        assert sum_basket == sum_price_goods

    @allure.description("Выбрать способ доставки 'Пункт выдачи'"
                        "Проверяется, что на странице отображается название выбраного пункта, т.е. поле не пустое")
    def test_selecting_delivery_point(self, auth, cart_clear, browser):
        # Кладем товар в корзину через бэк
        cart = Cart(auth)
        cart.cart_add(item=Items.point, quantity=3)

        # Выбираем способ доставки
        basket_page = BasketPage(browser)
        basket_page.go_to_basket_checked_all()
        basket_page.click(BasketPageLocators.AsideColumn.to_create_an_order)
        basket_page.select_delivery_method(delivery_method=DeliveryMethod.POINT)

        expect(basket_page.locator(BasketPageLocators.CreateOrder.name_point)).not_to_be_empty()

    @allure.description("Выбрать способ доставки 'Доставка'"
                        "Проверяется, что на странице отображается название выбраного адреса, т.е. поле не пустое ")
    def test_selecting_delivery_address(self, auth, cart_clear, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        # Заводим адрес
        profile_page = ProfilePage(browser)
        profile_page.click(MainPageLocators.Header.profile)
        profile_page.click(ProfilePageLocators.Address.add_address)
        profile_page.fill_in_address_card(title="Адрес доставки 2",
                                          address=InitialData.ProfileAddress.address_2,
                                          entrance="2",
                                          apartment="2",
                                          comment="Адрес создан UI-автотестами")
        # Кладем товар в корзину через бэк
        cart = Cart(auth)
        cart.cart_add(item=Items.delivery, quantity=3)
        # Выбираем способ доставки
        basket_page = BasketPage(browser)
        basket_page.go_to_basket_checked_all()
        basket_page.click(BasketPageLocators.AsideColumn.to_create_an_order)
        basket_page.select_delivery_method(delivery_method=DeliveryMethod.DELIVERY)

        expect(basket_page.locator(BasketPageLocators.CreateOrder.name_point)).not_to_be_empty()

    @allure.description("Выбрать способ доставки 'Самовывоз'"
                        "Проверяется, что на странице отображается название выбраного адреса, т.е. поле не пустое ")
    def test_selecting_self_delivery(self, auth, cart_clear, browser):
        # Кладем товар в корзину через бэк
        cart = Cart(auth)
        cart.cart_add(item=Items.self_delivery, quantity=3)

        # Выбираем способ доставки
        basket_page = BasketPage(browser)
        basket_page.go_to_basket_checked_all()
        basket_page.click(BasketPageLocators.AsideColumn.to_create_an_order)
        basket_page.select_delivery_method(delivery_method=DeliveryMethod.SELF_DELIVERY)

        expect(basket_page.locator(BasketPageLocators.CreateOrder.name_point)).not_to_be_empty()
