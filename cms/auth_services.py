
from helpers.request_service import rpc_request
from settings.env_config import settings


class CustomerAuth:

    def __init__(self, session):
        self.session = session

    def customer_login(self, login):
        """Авторизация клиента"""
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.login",
                               "params": {
                                   "login": login
                               }
                           })

    def customer_verify(self, password):
        """Подтверждение входа"""
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.verify",
                               "params": {
                                   "code": password
                               }
                           })

    def get_session(self):
        """Получить сессию"""
        return self.session
