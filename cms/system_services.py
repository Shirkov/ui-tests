import allure

from settings.env_config import settings
from helpers.request_service import rpc_request


class SystemCMS:
    """Системные методы, необходима авторизация системного пользователя"""

    def __init__(self, session):
        self.session = session

    def auth_login(self, login, password):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={"method": "auth.login",
                                   "params": {
                                       "username": login,
                                       "password": password
                                   }
                                   })

    @allure.step("Удалить заказы")
    def order_m_delete(self, order_id):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "orders.m_delete",
                               "params": {
                                   "id": order_id,
                               }
                           })

    def get_session(self):
        """Получить сессию"""
        return self.session
