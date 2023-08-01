import allure

from settings.env_config import settings
from helpers.request_service import rpc_request


class Address:

    def __init__(self, session):
        self.session = session

    @allure.step("Получение списка адресов")
    def addresses_list(self):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.addresses.list",
                               "params": {"page": 1, "page_size": 10}
                           })

    @allure.step("Удалить адрес")
    def addresses_delete(self, address_id):
        return rpc_request(session=self.session,
                           url=settings.cms.cms_url,
                           params={
                               "method": "customer.addresses.delete",
                               "params": {
                                   "address_id": address_id
                               }
                           })

    @allure.step("Удалить все адреса клиента, если они были созданы ранее")
    def addresses_m_delete(self):
        address_list = []
        rsp = self.addresses_list()
        for data in rsp['result']['data']:
            address_id = data['id']
            address_list.append(address_id)

        for address in address_list:
            adr_del = self.addresses_delete(address_id=address)
