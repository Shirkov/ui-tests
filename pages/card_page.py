from pages.base_page import BasePage


class VariantPageLocators:
    to_basket = "//button[text()='Добавить в корзину']"


class CardPageLocators:
    to_favorite_list = "//div[@class='product__content']//span[text()='В избранное']"
    product_slider_img = "//img[@class='product-slider__img']"
    close = "//img[@alt='close-modal']"
    to_basket = "//div[@class='product__content']//span[text()='В корзину']"
    share = "//div[@class='product__content']//button[@class='btn product__controls-btn']"
    share_link_list = "//div[@class='product__share-wrapper']//span[@class='text-md font-medium']"


class VariantPage(BasePage):
    pass


class CardPage(BasePage):
    pass
