import random
import time

import allure
import pytest
from playwright.sync_api import expect

from helpers.initial_data import InitialData
from pages.main_page import MainPage, MainPageLocators
from pages.profile_page import ProfilePage, ProfilePageLocators


@allure.epic("Тесты на страницу профиля")
@pytest.mark.usefixtures("addresses_delete")
class TestProfilePage:

    @allure.description("Изменение персональных данных"
                        "Проверяется что поменялись данные в полях ФИО, email, дата рождения")
    def test_change_personal_data(self, browser, faker):
        last_name = faker.last_name_male().replace("ё", "е")
        first_name = faker.first_name_male().replace("ё", "е")
        middle_name = faker.middle_name_male().replace("ё", "е")
        email = faker.email()
        birth_date = faker.date_of_birth().strftime('%d.%m.%Y')

        main_page = MainPage(browser)
        main_page.go_to()
        main_page.click(MainPageLocators.Header.profile)
        profile_page = ProfilePage(browser)
        profile_page.input_personal_data(last_name=f"{last_name}_тест",
                                         first_name=f"{first_name}_тест",
                                         middle_name=f"{middle_name}_тест",
                                         email=email,
                                         birth_date=birth_date)
        profile_page.click(ProfilePageLocators.ProfileTabs.save)

        expect(profile_page.page.locator(ProfilePageLocators.Info.last_name)).to_have_attribute("value",
                                                                                                f"{last_name}_тест")
        expect(profile_page.page.locator(ProfilePageLocators.Info.first_name)).to_have_attribute("value",
                                                                                                 f"{first_name}_тест")
        expect(profile_page.page.locator(ProfilePageLocators.Info.middle_name)).to_have_attribute("value",
                                                                                                  f"{middle_name}_тест")
        expect(profile_page.locator(ProfilePageLocators.Info.email)).to_have_attribute("value", email)
        expect(profile_page.locator(ProfilePageLocators.Info.birth_date)).to_have_attribute("value", birth_date)

    @allure.description("Создание 2х адресов в профиле пользователя. "
                        "Проверяется, что есть список из 2х адресов")
    def test_add_address_to_profile(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        profile_page = ProfilePage(browser)
        profile_page.click(MainPageLocators.Header.profile)
        profile_page.click(ProfilePageLocators.Address.add_address)
        profile_page.fill_in_address_card(title="Адрес доставки 1",
                                          address=InitialData.ProfileAddress.address_1,
                                          entrance="1",
                                          apartment="1",
                                          comment="Адрес создан UI-автотестами")

        profile_page.click(ProfilePageLocators.Address.add_address)
        profile_page.fill_in_address_card(title="Адрес доставки 2",
                                          address=InitialData.ProfileAddress.address_2,
                                          entrance="2",
                                          apartment="2",
                                          comment="Адрес создан UI-автотестами")
        expect(profile_page.locator(ProfilePageLocators.Address.address_list)).to_have_count(2)

    @allure.description("Удаление созданного адреса из профиля пользователя. "
                        "Проверяется, что после удаления остался только один адрес.")
    def test_delete_address_to_profile(self, browser):
        main_page = MainPage(browser)
        main_page.go_to()
        profile_page = ProfilePage(browser)
        profile_page.click(MainPageLocators.Header.profile)
        profile_page.click(ProfilePageLocators.Address.delete)

        expect(profile_page.locator(ProfilePageLocators.Address.address_list)).to_have_count(1)
