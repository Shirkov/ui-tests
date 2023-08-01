import allure

from pages.base_page import BasePage


class OrdersPageLocators:
        order_list = "//div[@class='order-history']"
        three_dots = "//div[@class='order-history__btn']"
        cancel_order = "//div[@class='order-history__delete-item']"
        confirm_cancel_order = "//button[text()='Отменить заказ']"
        necessarily = "//button[text()='Обязательно!']"
        status_cancelled = "//div[@class='detail__status order__status order__status_cancelled']"
        status_order = "//div[@class='detail__status order__status']"


class OrdersPageScripts:
    order_status = "document.querySelector('.order-history__status.order-history__status-await').textContent"


class OrdersPage(BasePage):

    @allure.step("Отмена заказа")
    def cancel_order(self):
        self.click(OrdersPageLocators.three_dots)
        self.click(OrdersPageLocators.cancel_order)
        self.click(OrdersPageLocators.confirm_cancel_order)
        self.click(OrdersPageLocators.necessarily)
