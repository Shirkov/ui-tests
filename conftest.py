import os

import pytest
import requests
from faker import Faker
from playwright.sync_api import Playwright

from cms.auth_services import CustomerAuth
from cms.cart_services import Cart
from cms.favorite_services import Favorite
from cms.orders_services import Orders
from cms.system_services import SystemCMS

from pages.main_page import MainPage
from settings.env_config import settings
from cms.addresses_services import Address
from start_tests import LOG


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    """Инициализация браузера инкогнито"""
    global context, page
    for retry in range(1):
        try:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.set_default_timeout(20000)

            main_page = MainPage(page)
            main_page.authorize_user(username=settings.browser.login)

        except Exception as err:
            LOG.info(f"Авторизация пользователя не произошла, ошибка: {err}")
            context.close()
            page.close()

            continue

        yield page
        context.close()
        page.close()


@pytest.fixture(scope="session", autouse=True)
def auth():
    """Авторизация пользователя"""
    session = requests.Session()
    auth = CustomerAuth(session=session)
    auth.customer_login(login=settings.cms.cms_login)
    verify = auth.customer_verify(password=settings.cms.cms_password)

    assert verify['result']['verified'] is True, "Пользователь в CMS не авторизовался"

    return auth.get_session()


@pytest.fixture(scope="session", autouse=True)
def sys_auth():
    """Авторизация системного пользователя"""
    session = requests.Session()
    sys_cms = SystemCMS(session=session)
    sys_cms.auth_login(login=settings.cms.cms_sys_login, password=settings.cms.cms_sys_password)

    return sys_cms.get_session()


@pytest.fixture(scope="class")
def addresses_delete(auth):
    """Удаление ранее созданных адресов"""
    address = Address(auth)
    address.addresses_m_delete()


@pytest.fixture()
def favorite_clear(auth):
    """Очистка избранного"""
    favorite = Favorite(auth)
    favorite.favorites_clear()


@pytest.fixture()
def cart_clear(auth):
    """Очистка всей корзины """
    cart = Cart(auth)
    cart.clear()


@pytest.fixture()
def faker():
    """Инициализация генератора фейковвых данных"""
    return Faker("ru_RU")


@pytest.fixture()
def delete_orders(auth, sys_auth):
    """
    Перевод всех заказов в статус 'canceled' и их последующее удаление"""
    orders_id_list = []

    orders = Orders(auth)
    rsp = orders.orders_list()
    for order in rsp["result"]["data"]:
        if order["order"]["ext_status"] != "canceled":
            orders.orders_cancel(order_id=order["order"]["id"])
        orders_id_list.append(order["order"]["id"])

    if orders_id_list:
        sys_cms = SystemCMS(sys_auth)
        sys_cms.order_m_delete(order_id=orders_id_list)


@pytest.fixture(scope="class")
def post_delete_orders(auth, sys_auth):
    """
    Перевод всех заказов в статус 'canceled' и их последующее удаление
    Выполнение в конце тестового класса"""
    yield
    orders_id_list = []

    orders = Orders(auth)
    rsp = orders.orders_list()
    for order in rsp["result"]["data"]:
        if order["order"]["ext_status"] != "canceled":
            orders.orders_cancel(order_id=order["order"]["id"])
        orders_id_list.append(order["order"]["id"])

    if orders_id_list:
        sys_cms = SystemCMS(sys_auth)
        sys_cms.order_m_delete(order_id=orders_id_list)
