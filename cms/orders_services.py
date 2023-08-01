import allure

from settings.env_config import settings
from helpers.request_service import rpc_request


class Orders:

    def __init__(self, session):
        self.session = session

    @allure.step("Получение списка адресов")
    def orders_list(self):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.orders.list",
                               "params": {"page": 1,
                                          "page_size": 100,
                                          "client_type": "site"}
                           })

    @allure.step("Отменить заказ")
    def orders_cancel(self, order_id):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.orders.cancel",
                               "params": {"order_id": order_id,
                                          "reason_id": "other"}
                           })
