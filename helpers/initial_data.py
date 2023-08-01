class InitialData:
    class ProfileAddress:
        address_1 = "г Москва, 3-й Митинский пер, д 2"
        address_2 = "Москва, Ленинский пр-кт, 88А"


class DeliveryMethod:
    POINT = "POINT"
    DELIVERY = "DELIVERY"
    SELF_DELIVERY = "SELF_DELIVERY"


class Items:
    """id товаров под определенный тип доставки"""
    point = "259-207"  # Фен с двумя скоростями
    delivery = "268-057"  # Очень точные весы для кухни
    self_delivery = "268-057"  # Очень точные весы для кухни


class StatusPay:
    await_pay = "Ждет оплаты"


class StatusOrder:
    canceled = "Отменен"
    new = "Новый"


class Links:
    vk = "https://vk.com/vsegazin"
    tg = "https://t.me/vsegazin"
    app_store = "https://apps.apple.com/ru/app/id6449432697"
    g_play = "https://play.google.com/store/apps/details?id=ru.vsegazin.app"
    nash_store = "https://store.nashstore.ru/store/6441849efb3ed3a10c635674"


class SocialGroupList:
    """Название социальной сети по номеру индекса"""
    VK = 0
    TELEGRAM = 1


class MobileAppList:
    """Название магазинов приложений по номеру индекса"""
    APP_STORE = 0
    G_PLAY = 1
    NASH_STORE = 2
