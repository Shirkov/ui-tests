import time

import allure
import pytest

from cms.cart_services import Cart
from helpers.initial_data import DeliveryMethod, Items, StatusOrder, StatusPay, InitialData
from pages.basket_page import BasketPageLocators, BasketPage
from pages.main_page import MainPage, MainPageLocators
from playwright.sync_api import expect

from pages.orders_page import OrdersPage, OrdersPageScripts, OrdersPageLocators
from pages.profile_page import ProfilePage, ProfilePageLocators


@allure.epic("Тесты на страницу оформления заказа")
@pytest.mark.usefixtures("addresses_delete")
@pytest.mark.usefixtures("post_delete_orders")
class TestOrderCreatePage:

    @allure.description("Создание заказа в пункт выдачи с оплатой онлайн(оплату не проводим). "
                        "Проверяется страница заказа, что список заказов не пустой,"
                        "статус оплаты - 'Ждет оплаты', "
                        "статус заказа - 'Новый'"
                        "отменяем заказ, проверяем, что заказ отменен")
    def test_create_order_to_point_with_online_payment(self, auth, cart_clear, delete_orders, browser):
        # Кладем товар в корзину через бэк
        cart = Cart(auth)
        cart.cart_add(item=Items.point, quantity=3)

        main_page = MainPage(browser)
        main_page.go_to()
        time.sleep(1)
        # Выбираем способ доставки "Пункт выдачи"
        basket_page = BasketPage(browser)
        basket_page.go_to_basket_checked_all()
        basket_page.click(BasketPageLocators.AsideColumn.to_create_an_order)
        basket_page.select_delivery_method(delivery_method=DeliveryMethod.POINT)
        # Выбираем способ оплаты и создаем заказ
        basket_page.click(BasketPageLocators.CreateOrder.Payment.online)
        basket_page.click(BasketPageLocators.CreateOrder.Payment.bank_card)
        basket_page.click(BasketPageLocators.CreateOrder.online_pay)
        main_page.go_to()
        time.sleep(5)
        # Проверяем, что есть заказ
        main_page.click(MainPageLocators.Header.orders)
        orders_page = OrdersPage(browser)
        time.sleep(1)
        order_status_pay = orders_page.evaluate(script=OrdersPageScripts.order_status)
        expect(basket_page.locator(OrdersPageLocators.order_list)).not_to_have_count(0, timeout=10000)
        assert order_status_pay == StatusPay.await_pay

        orders_page.click(OrdersPageLocators.order_list, index=0)
        expect(orders_page.locator(OrdersPageLocators.status_order)).to_have_text(StatusOrder.new, timeout=5000)
        main_page.click(MainPageLocators.Header.orders)
        # Отменяем его, проверяем статус отмены
        orders_page.cancel_order()
        expect(orders_page.locator(OrdersPageLocators.status_cancelled)).to_have_text(StatusOrder.canceled,
                                                                                      timeout=5000)

    @allure.description("Создание заказа на доставку курьером с оплатой онлайн(оплату не проводим). "
                        "Проверяется страница заказа, что список заказов не пустой,"
                        "отменяем заказ, проверяем, что заказ отменен")
    def test_create_order_to_delivery_with_online_payment(self, auth, cart_clear, delete_orders, browser):
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
        # Выбираем способ оплаты и создаем заказ
        basket_page.click(BasketPageLocators.CreateOrder.Payment.online)
        basket_page.click(BasketPageLocators.CreateOrder.Payment.bank_card)
        basket_page.click(BasketPageLocators.CreateOrder.online_pay)
        main_page.go_to()
        time.sleep(5)
        # Проверяем, что есть заказ и отменяем его, проверяем статус отмены
        main_page.click(MainPageLocators.Header.orders)
        orders_page = OrdersPage(browser)
        expect(orders_page.locator(OrdersPageLocators.order_list)).not_to_be_empty(timeout=5000)

        orders_page.cancel_order()
        expect(orders_page.locator(OrdersPageLocators.status_cancelled)).to_have_text(StatusOrder.canceled,
                                                                                      timeout=5000)

    @allure.description("Создание заказа самовывоз с оплатой  наличными"
                        "Проверяется страница заказа, что список заказов не пустой,"
                        "отменяем заказ, проверяем, что заказ отменен")
    def test_create_order_to_self_delivery_with_cash_payment(self, auth, cart_clear, delete_orders, browser):
        # Кладем товар в корзину через бэк
        cart = Cart(auth)
        cart.cart_add(item=Items.self_delivery, quantity=3)

        # Выбираем способ доставки "Самовывоз"
        basket_page = BasketPage(browser)
        basket_page.go_to_basket_checked_all()
        basket_page.click(BasketPageLocators.AsideColumn.to_create_an_order)
        basket_page.select_delivery_method(delivery_method=DeliveryMethod.SELF_DELIVERY)
        # Выбираем способ оплаты и создаем заказ
        basket_page.click(BasketPageLocators.CreateOrder.Payment.upon_delivery)
        basket_page.click(BasketPageLocators.CreateOrder.Payment.cash)
        basket_page.click(BasketPageLocators.CreateOrder.create_order)
        main_page = MainPage(browser)
        main_page.go_to()
        time.sleep(5)
        # Проверяем, что есть заказ и отменяем его, проверяем статус отмены
        main_page.click(MainPageLocators.Header.orders)
        orders_page = OrdersPage(browser)
        expect(orders_page.locator(OrdersPageLocators.order_list)).not_to_be_empty(timeout=5000)

        orders_page.cancel_order()
        expect(orders_page.locator(OrdersPageLocators.status_cancelled)).to_have_text(StatusOrder.canceled,
                                                                                      timeout=5000)
