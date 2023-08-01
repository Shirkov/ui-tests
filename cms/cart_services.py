import allure

from settings.env_config import settings
from helpers.request_service import rpc_request


class Cart:

    def __init__(self, session):
        self.session = session

    @allure.step("Очистка всей корзины")
    def clear(self):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.cart.clear",
                               "params": {
                               }
                           })

    @allure.step("В корзину добавить товар {item} в количестве {quantity} шт")
    def cart_add(self, item: str, quantity: int):
        return rpc_request(url=settings.cms.cms_url,
                           session=self.session,
                           params={
                               "method": "customer.cart.add",
                               "params": {
                                   "items": [
                                       {"id": item, "quantity": quantity}
                                   ]
                               }
                           })
