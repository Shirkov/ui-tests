from pages.base_page import BasePage


class ContactsPageLocators:
    contacts_item_list = "//div[@class='contacts__item']"
    contacts_social_list = "//a[@class='contacts__social']"
    addresses_and_phones = "//div[@class='contacts__description']//a[text()='Адреса и телефоны магазинов']"
    franchise = "//div[@class='contacts__description']//a[text()='сети \"Галамарт\"']"
    rental = "//div[@class='contacts__description']//a[text()='Аренда']"
    service_centres = "//div[@class='contacts__description']//a[text()='Сервисных центрах']"


class ContactsPage(BasePage):
    pass
