import time

import allure

from helpers.initial_data import DeliveryMethod
from pages.base_page import BasePage
from playwright.sync_api import expect

from settings.env_config import settings


class BasketPageLocators:
    class Card:
        card_list = "//div[@class='bucket-product']"
        to_favorite_list = "//img[@alt='В избранное']"
        plus_list = "//button[@class='btn btn--transparent bucket-product__btn'][2]"
        minus_list = "//button[@class='btn btn--transparent bucket-product__btn'][1]"
        price_list = "//div[@class='title-lg bucket-product__price-current']"
        count_list = "//div[@class='bucket-product__quantity']//span[@class='font-bold text-sm']"
        delete_list = "//button[@class='btn btn--icon bucket-product__remove-btn']"
        delete_all = "//span[text()='Удалить']"
        empty_basket_alert = "//p[@class='text-sm font-bold']"

    class AsideColumn:
        quantity = "//div[@class='bucket__params-item text-sm font-medium'][1]//span[2]"
        price = "//div[@class='bucket__params-item text-sm font-medium'][2]//span[2]"
        total = "//div[@class='bucket__total']//span[2]"
        to_create_an_order = "//button[text()='К оформлению']"

    class CreateOrder:
        pickup_point = "//button[text()='Пункт выдачи']"
        select_delivery_point = "//button[text()='Выбрать пункт доставки']"
        name_point = "//h2[@class='text-md font-extra-black']"
        delivery = "//button[text()='Доставка']"
        select_address_delivery = "//button[text()='Выбрать адрес доставки']"
        online_pay = "//button[text()='Оплатить онлайн']"
        create_order = "//button[text()='Оформить заказ']"
        self_delivery = "//button[text()='Самовывоз']"
        select_store = "//button[text()='Выбрать магазин']"

        class DeliveryPoint:
            search = "//div[@class='pickup-modal']//input[@placeholder='Поиск']"
            select_point = "//button[text()='Выбрать']"

        class AddressDelivery:
            address_delivery = "//span[text()='Адрес доставки 2']"
            select_address = "//button[text()='Выбрать']"
            day_delivery_list = "//div[@class='delivery-time-modal__day delivery-time-modal__day']"
            time_delivery_list = "//div[@class='delivery-time-modal__period  font-bold text-lg']"

        class Payment:
            online = "//button[text()='Онлайн']"
            upon_delivery = "//button[text()='При получении']"
            bank_card = "//label[@for='online-payment']"
            cash = "//label[@for='cod-payment-cash']"


class BasketPage(BasePage):

    @allure.step("Переход в корзину с активацией товаров")
    def go_to_basket_checked_all(self):
        self.page.goto(f"{settings.browser.base_url}cart/?checkedAll=true")
        return self.page.goto(f"{settings.browser.base_url}cart/?checkedAll=true")

    @staticmethod
    def _replace_string_price_to_int(string: str):
        non_breaking_space = "\xa0"
        price = int(string.replace(" ₽", "").replace(non_breaking_space, ""))
        return price

    def sum_price(self, obj_locator):
        price_list = []
        for locator in obj_locator.all():
            text = self._replace_string_price_to_int(string=locator.inner_text())
            price_list.append(text)

        return sum(price_list)

    @allure.step("Выбор способа доставки")
    def select_delivery_method(self, delivery_method):
        if delivery_method == DeliveryMethod.POINT:
            self.click(BasketPageLocators.CreateOrder.pickup_point)
            self.click(BasketPageLocators.CreateOrder.select_delivery_point)
            time.sleep(5)
            self.mouse_click(x=939, y=449)
            self.click(BasketPageLocators.CreateOrder.DeliveryPoint.select_point)

        if delivery_method == DeliveryMethod.DELIVERY:
            self.click(BasketPageLocators.CreateOrder.delivery)
            self.click(BasketPageLocators.CreateOrder.select_address_delivery)
            time.sleep(5)
            self.click(BasketPageLocators.CreateOrder.AddressDelivery.address_delivery)
            self.click(BasketPageLocators.CreateOrder.AddressDelivery.select_address)
            self.click(BasketPageLocators.CreateOrder.AddressDelivery.day_delivery_list)
            self.click(BasketPageLocators.CreateOrder.AddressDelivery.time_delivery_list)
            self.click(BasketPageLocators.CreateOrder.AddressDelivery.select_address)

        if delivery_method == DeliveryMethod.SELF_DELIVERY:
            time.sleep(2)
            self.click(BasketPageLocators.CreateOrder.self_delivery)
            time.sleep(2)
            self.click(BasketPageLocators.CreateOrder.select_store)
            time.sleep(5)
            self.mouse_click(x=1184, y=697)
            self.click(BasketPageLocators.CreateOrder.DeliveryPoint.select_point)

