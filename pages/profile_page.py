import time

import allure

from pages.base_page import BasePage
from playwright.sync_api import expect


class ProfilePageLocators:
    class ProfileTabs:
        personal_data = "//a[text()='Личная информация']"
        favorite = "//a[text()='Избранное']"
        orders = "//a[text()='Заказы']"
        save = "//button[text()='Cохранить']"
        cancel = "//button[text()='Отмена']"

    class Info:
        last_name = "//input[@name='last_name']"
        first_name = "//input[@name='first_name']"
        middle_name = "//input[@name='middle_name']"
        email = "//input[@name='email']"
        phone = "//input[@name='phone']"
        birth_date = "//input[@name='birth_date']"

    class Address:
        add_address = "//img[@alt='Добавить адрес']"
        title = "//input[@placeholder='Название*']"
        address = "//input[@placeholder='Адрес*']"
        drop_down_list = "//button[@class='react-dadata__suggestion']"
        entrance = "//input[@placeholder='Подъезд']"
        apartment = "//input[@placeholder='Квартира']"
        comment = "//textarea[@placeholder='Комментарий']"
        add_address_button = "//button[text()='Добавить']"
        address_list = "//div[@class='profile-address__item']"
        delete = "//div[@class='profile-address__item'][1]//button[@class='btn btn--icon'][2]"

    class Favorite:
        card_list = "//div[@class='card']"
        to_favorite_list = "//div[@class='favorite card__favorite']"
        to_basket_list = "//div[@class='card-actions']"
        empty_block = "//span[text()='Вы еще ничего не добавили в избранное']"


class ProfilePage(BasePage):

    @allure.step("Ввод персональных данных")
    def input_personal_data(self, last_name, first_name, middle_name, email, birth_date):
        self.input_text_after_clear(ProfilePageLocators.Info.last_name, text=last_name)
        self.input_text_after_clear(ProfilePageLocators.Info.first_name, text=first_name)
        self.input_text_after_clear(ProfilePageLocators.Info.middle_name, text=middle_name)
        self.input_text_after_clear(ProfilePageLocators.Info.email, text=email)
        self.input_text_after_clear(ProfilePageLocators.Info.birth_date, text=birth_date)

    @allure.step("Заполнение карточки создания/ редактирования адреса")
    def fill_in_address_card(self, title, address, entrance, apartment, comment):
        self.input_text(ProfilePageLocators.Address.title, text=title)
        self.input_text(ProfilePageLocators.Address.address, text=address)
        expect(self.locator(ProfilePageLocators.Address.drop_down_list).nth(0)).to_be_enabled(timeout=10000)
        self.click(ProfilePageLocators.Address.drop_down_list, index=0)
        self.input_text(ProfilePageLocators.Address.entrance, text=entrance)
        self.input_text(ProfilePageLocators.Address.apartment, text=apartment)
        self.input_text(ProfilePageLocators.Address.comment, text=comment)
        self.click(ProfilePageLocators.Address.add_address_button)
