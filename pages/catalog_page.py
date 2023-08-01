import time

import allure

from pages.base_page import BasePage


class CatalogPageLocator:
    card_list = "//div[@class='card']"
    filter_list = "//label[@class='custom-control-label']"
    card_link_list = "//a[@class='card__title text-sm']"
    favorites_list = "//div[@class='favorite card__favorite']"


class CatalogPage(BasePage):
    pass
