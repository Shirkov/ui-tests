import allure
from playwright.sync_api import expect

from helpers.initial_data import SocialGroupList, Links, MobileAppList
from pages.main_page import MainPage, MainPageLocators


@allure.epic("Тесты на футер главной страницы")
class TestFooter:

    @allure.description("Наличие ссылок на социальные сети. "
                        "Проверяются ссылки на VK и Telegram")
    def test_social_media_links(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        expect(main_page.locator(MainPageLocators.Footer.socials_item_list).nth(SocialGroupList.VK)) \
            .to_have_attribute(name="href", value=Links.vk)
        expect(main_page.locator(MainPageLocators.Footer.socials_item_list).nth(SocialGroupList.TELEGRAM)) \
            .to_have_attribute(name="href", value=Links.tg)

    @allure.description("Наличие ссылок на магазины приложений. "
                        "Проверяются ссылки на APP_STORE, GOOGLE_PLAY, NASH_STORE")
    def test_app_store_links(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        expect(main_page.locator(MainPageLocators.Footer.apps_items_list).nth(MobileAppList.APP_STORE)) \
            .to_have_attribute(name="href", value=Links.app_store)
        expect(main_page.locator(MainPageLocators.Footer.apps_items_list).nth(MobileAppList.G_PLAY)) \
            .to_have_attribute(name="href", value=Links.g_play)
        expect(main_page.locator(MainPageLocators.Footer.apps_items_list).nth(MobileAppList.NASH_STORE)) \
            .to_have_attribute(name="href", value=Links.nash_store)
