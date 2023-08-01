import allure

from settings.env_config import settings
from helpers.request_service import rpc_request


class Favorite:

    def __init__(self, session):
        self.session = session

    @allure.step("Очистка избранного")
    def favorites_clear(self):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.favorites.clear"
                           })
